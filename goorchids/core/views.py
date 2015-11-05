import gzip
import sys
import argparse
import traceback
import time
import warnings
from datetime import datetime
from StringIO import StringIO
from contextlib import contextmanager, closing

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from django.core import serializers
from django.core.management.commands.loaddata import Command as LoadCommand
from django.core.files.storage import default_storage
from django.db import (connections, router, transaction, DEFAULT_DB_ALIAS,
                       DatabaseError, IntegrityError)
from django.utils.encoding import force_text

from gobotany.core.models import (TaxonCharacterValue, CharacterValue,
                                  CopyrightHolder, ContentImage, GlossaryTerm,
                                  Genus)
from gobotany.site.models import PlantNameSuggestion, SearchSuggestion
from gobotany.search.models import (PlainPage, GroupsListPage,
                                    SubgroupsListPage, SubgroupResultsPage)
from gobotany.core.importer import Importer
from .models import RegionalConservationStatus, ImportLog

from rq import Queue
from redis.exceptions import ConnectionError
from worker import conn

q = Queue('low', connection=conn)


APPS_TO_HANDLE = ['goorchids_core', 'core', 'search', 'simplekey', 'dkey',
                  'goorchids_site', 'site', 'flatpages', 'sites']
EXCLUDED_MODELS = ['core.PartnerSite', 'goorchids_core.ImportLog',
                   'site.SearchSuggestion', 'site.PlantNameSuggestion']
DUMP_NAME = 'goorchids-core-data-{:%Y%m%d%H%M%S}.json'
DUMP_PATH = '/core-data/'


@permission_required('superuser')
def dumpdata(request):
    # Rebuild the search suggestion tables before dump
    Importer().import_search_suggestions()
    Importer().import_plant_name_suggestions()
    try:
        job = q.enqueue(_dump)
        message = 'Export job started (job id: %s)' % job.id
    except ConnectionError:
        message = _dump()

    return JsonResponse(message,
                        safe=False,
                        content_type='text/plain; charset=utf-8')


def _dump():
    s_time = time.time()
    from django.apps import apps
    from django.db.models import get_model
    excluded_models = set()
    for exclude in EXCLUDED_MODELS:
        app_label, model_name = exclude.split('.', 1)
        model_obj = get_model(app_label, model_name)
        excluded_models.add(model_obj)

    app_list = [(c, None) for c in apps.get_app_configs() if c.label in
                set(APPS_TO_HANDLE)]

    objects = []
    for model in serializers.sort_dependencies(app_list):
        if model in excluded_models:
            continue
        if not model._meta.proxy and router.allow_migrate(DEFAULT_DB_ALIAS, model):
            objects.extend(model._default_manager.using(DEFAULT_DB_ALIAS).all())

    f_name = DUMP_NAME.format(datetime.now())
    with closing(StringIO()) as compressed_data:
        with gzip.GzipFile(filename=f_name, mode='wb',
                           fileobj=compressed_data) as compressor:
            compressor.write(serializers.serialize('json', objects, indent=2,
                                                   use_natural_foreign_keys=True))
        compressed_data.seek(0)
        default_storage.save(DUMP_PATH + f_name + '.gz', compressed_data)

    return '%d objects exported to %s in %d seconds'%(len(objects), f_name,
                                                      time.time() - s_time)


def list_data_files():
    directories, filenames = default_storage.listdir(DUMP_PATH)
    return list(reversed(sorted([ f for f in filenames if
                                  f.endswith('.json.gz') ])))


@contextmanager
def get_latest_fixture(name=None):
    if name is None:
        name = list_data_files()[0]
    compressed = default_storage.open(DUMP_PATH + name)
    decompressor = gzip.GzipFile(fileobj=compressed, mode='rb')
    try:
        yield decompressor
    finally:
        decompressor.close()
        compressed.close()


@permission_required('superuser')
def loaddata(request):
    message = ''
    files = list_data_files()
    if 'filename' in request.POST:
        filename = request.POST['filename']
        log_entry = ImportLog(filename=filename, start=datetime.now())
        try:
            job = q.enqueue_call(func=_load, args=(filename, log_entry),
                                 timeout=3600) # 10 minute timeout
            message = (u'Data import running in background (Job Id: %s).  '
                       'Data load will complete in a few minutes.'%job.id)
        except ConnectionError:
            # Redis not running, try to run synchronously
            message = _load(filename, log_entry)
            message += ' (async data load failed)'

    latest_logs = ImportLog.objects.order_by('-start')[:5]
    return render_to_response('goorchids/loaddata.html', {'files': files,
                                                          'message': message,
                                                          'logs': latest_logs},
                              context_instance=RequestContext(request))


class GoOrchidsLoader(LoadCommand):

    def load_label(self, fixture_label, ser_fmt='json'):
        """
        Uses get_latest_fixture to load fixture data
        """

        with get_latest_fixture(fixture_label) as fixture:
            try:
                self.fixture_name = fixture.name
                self.fixture_count += 1
                objects_in_fixture = 0
                loaded_objects_in_fixture = 0
                if self.verbosity >= 2:
                    self.stdout.write("Installing %s fixture." % (
                        fixture.name
                    ))

                objects = serializers.deserialize(
                    ser_fmt, fixture, using=self.using,
                    ignorenonexistent=self.ignore
                )

                for obj in objects:
                    objects_in_fixture += 1
                    if router.allow_migrate_model(self.using,
                                                  obj.object.__class__):
                        loaded_objects_in_fixture += 1
                        self.models.add(obj.object.__class__)
                        try:
                            obj.save(using=self.using)
                        except (DatabaseError, IntegrityError) as e:
                            e.args = ("Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s" % {
                                'app_label': obj.object._meta.app_label,
                                'object_name': obj.object._meta.object_name,
                                'pk': obj.object.pk,
                                'error_msg': force_text(e)
                            },)
                            raise

                self.loaded_object_count += loaded_objects_in_fixture
                self.fixture_object_count += objects_in_fixture
            except Exception as e:
                e.args = ("Problem installing fixture '%s': %s" % (fixture.name, e),)
                raise
            finally:
                fixture.close()

            # Warn if the fixture we loaded contains 0 objects.
            if objects_in_fixture == 0:
                warnings.warn(
                    "No fixture data found for '%s'. (File format may be "
                    "invalid.)" % fixture.name,
                    RuntimeWarning
                )


def _load(name, log_entry=None, verbosity=2):
    using = DEFAULT_DB_ALIAS
    loader = GoOrchidsLoader()
    loader.using = using
    loader.ignore = False
    loader.app_label = None
    loader.hide_empty = False
    loader.verbosity = verbosity
    s_time = time.time()
    try:
        with transaction.atomic(using=using):
            # First remove all character values, assignments, images and
            # generated values to avoid import conflicts and data
            # duplication
            Genus.objects.all().delete()
            TaxonCharacterValue.objects.all().delete()
            CharacterValue.objects.all().delete()
            CopyrightHolder.objects.all().delete()
            ContentImage.objects.all().delete()
            PlantNameSuggestion.objects.all().delete()
            SearchSuggestion.objects.all().delete()
            RegionalConservationStatus.objects.all().delete()
            PlainPage.objects.all().delete()
            GroupsListPage.objects.all().delete()
            SubgroupsListPage.objects.all().delete()
            SubgroupResultsPage.objects.all().delete()
            GlossaryTerm.objects.all().delete()

            # Load the data
            loader.loaddata([name])

            # If the fixture we loaded contains 0 objects, assume that an
            # error was encountered during fixture loading and raise a DB
            # error to force a rollback.
            if loader.fixture_object_count == 0:
                raise DatabaseError("No fixture data found. (File format may be invalid.)")

        if transaction.get_autocommit(using):
            connections[using].close()
    except (SystemExit, KeyboardInterrupt):
        raise
    except:
        msg = "Problem installing fixture: %s" % (
            ''.join(traceback.format_exception(sys.exc_type,
                                               sys.exc_value,
                                               sys.exc_traceback)))
        if log_entry:
            log_entry.success = False
            log_entry.message = msg
            log_entry.duration = time.time() - s_time
            log_entry.save()
        return msg

    # Rebuild the search suggestion tables
    Importer().import_search_suggestions()
    Importer().import_plant_name_suggestions()

    end_time = time.time()
    msg = 'Successfully Loaded %s objects from fixture %s in %d seconds'%(
        loader.loaded_object_count, loader.fixture_name, end_time - s_time
    )

    if log_entry:
        log_entry.success = True
        log_entry.message = msg
        log_entry.duration = end_time - s_time
        log_entry.save()

    return msg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="importer",
        description='Import GoOrchids fixture by name'
    )

    parser.add_argument('filename', nargs="?")
    args = parser.parse_args()
    if not args.filename:
        name = list_data_files()[0]
    else:
        name = args.filename
    print(_load(name))

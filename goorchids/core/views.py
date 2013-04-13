import gzip
import sys
import traceback
from StringIO import StringIO
from datetime import datetime
from contextlib import contextmanager, closing

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core import serializers
from django.core.management.commands.dumpdata import sort_dependencies
from django.core.management.color import no_style
from django.core.files.storage import default_storage
from django.db import (connections, router, transaction, DEFAULT_DB_ALIAS,
      IntegrityError, DatabaseError)
from django.utils.datastructures import SortedDict


APPS_TO_HANDLE = ['core', 'search', 'simplekey', 'plantoftheday', 'dkey',
                  'site', 'flatpages', 'sites']
EXCLUDED_MODELS = ['core.PartnerSite',]
DUMP_NAME = 'goorchids-core-data-{:%Y%m%d%H%M%S}.json'
DUMP_PATH = '/core-data/'

@permission_required('superuser')
def dumpdata(request):
    from django.db.models import get_app, get_model
    excluded_models = set()
    for exclude in EXCLUDED_MODELS:
        app_label, model_name = exclude.split('.', 1)
        model_obj = get_model(app_label, model_name)
        excluded_models.add(model_obj)

    app_list = SortedDict()
    for app_label in APPS_TO_HANDLE:
        app = get_app(app_label)
        app_list[app] = None

    objects = []
    for model in sort_dependencies(app_list.items()):
        if model in excluded_models:
            continue
        if not model._meta.proxy and router.allow_syncdb(DEFAULT_DB_ALIAS, model):
            objects.extend(model._default_manager.using(DEFAULT_DB_ALIAS).all())

    f_name = DUMP_NAME.format(datetime.now())
    with closing(StringIO()) as compressed_data:
        with gzip.GzipFile(filename=f_name, mode='wb',
                           fileobj=compressed_data) as compressor:
            compressor.write(serializers.serialize('json', objects, indent=2,
                                                   use_natural_keys=True))
        compressed_data.seek(0)
        default_storage.save(DUMP_PATH + f_name + '.gz', compressed_data)

    return HttpResponse('Data exported as %s.gz'%f_name,
                        mimetype='text/plain; charset=utf-8')

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
        message = _load(filename)

    return render_to_response('goorchids/loaddata.html', {'files': files,
                                                          'message': message},
                              context_instance=RequestContext(request))

def _load(name):
    # code blatantly stolen from django.core.management.commands.loaddatax
    style = no_style()
    using = DEFAULT_DB_ALIAS
    connection = connections[DEFAULT_DB_ALIAS]
    models = set()

    # Get a cursor (even though we don't need one yet). This has
    # the side effect of initializing the test database (if
    # it isn't already initialized).
    cursor = connection.cursor()

    # Start transaction management. All fixtures are installed in a
    # single transaction to ensure that all references are resolved.
    transaction.commit_unless_managed(using=using)
    transaction.enter_transaction_management(using=using)
    transaction.managed(True, using=using)

    try:
        with connection.constraint_checks_disabled():
            objects_in_fixture = 0
            loaded_objects_in_fixture = 0
            with get_latest_fixture(name) as fixture:
                fixture_name = fixture.filename
                objects = serializers.deserialize('json', fixture,
                                                  using=using)
                for obj in objects:
                    objects_in_fixture += 1
                    if router.allow_syncdb(using, obj.object.__class__):
                        loaded_objects_in_fixture += 1
                        models.add(obj.object.__class__)
                        try:
                            obj.save(using=using)
                        except (DatabaseError, IntegrityError), e:
                            msg = "Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s" % {
                                'app_label': obj.object._meta.app_label,
                                'object_name': obj.object._meta.object_name,
                                'pk': obj.object.pk,
                                'error_msg': e
                            }
                            raise e.__class__, e.__class__(msg), sys.exc_info()[2]


            # If the fixture we loaded contains 0 objects, assume that an
            # error was encountered during fixture loading.
            if objects_in_fixture == 0:
                transaction.rollback(using=using)
                transaction.leave_transaction_management(using=using)
                return "No fixture data found. (File format may be invalid.)"

        # Since we disabled constraint checks, we must manually check for
        # any invalid keys that might have been added
        table_names = [model._meta.db_table for model in models]
        connection.check_constraints(table_names=table_names)

    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        transaction.rollback(using=using)
        transaction.leave_transaction_management(using=using)
        msg = "Problem installing fixture: %s" %(
            ''.join(traceback.format_exception(sys.exc_type,
                                               sys.exc_value,
                                               sys.exc_traceback)))
        return msg

    # If we found even one object in a fixture, we need to reset the
    # database sequences.
    if loaded_objects_in_fixture > 0:
        sequence_sql = connection.ops.sequence_reset_sql(style, models)
        if sequence_sql:
            for line in sequence_sql:
                cursor.execute(line)

    transaction.commit(using=using)
    transaction.leave_transaction_management(using=using)
    return 'Successfully Loaded %s objects from fixture %s'%(
        loaded_objects_in_fixture,
        fixture_name)

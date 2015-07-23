# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import DataMigration
from django.db import models
from gobotany.core.importer import Importer
from gobotany.taxa.templatetags.taxa_tags import s_rank_label
from gobotany.taxa.templatetags.taxa_tags import endangerment_code_label


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for c_status in orm['core.ConservationStatus'].objects.all():
            label = c_status.label
            if label:
                code = ''
                s_rank = ''
                label = label.lower()
                if 'historical' in label:
                    code = '- H'
                elif 'watch list' in label:
                    code = '- WL'
                elif 'special concern' in label:
                    code = 'SC'
                elif 'special concern' in label and 'extirpated' in label:
                    code = 'SC*'
                elif 'concern' in label:
                    code = 'C'
                elif 'concern (uncertain)' in label:
                    code = 'C*'
                elif 'federally endangered' in label:
                    code = 'FE'
                elif 'state endangered' in label:
                    code = 'SE'
                elif 'endangered' in label:
                    code = 'E'
                elif ('federally threatened' in label and
                      'historic' in label):
                    code = 'FT/SH'
                elif 'federally threatened' in label:
                    code = 'FT'
                elif 'potentially extirpated' in label:
                    code = 'PE'
                elif 'historic' in label:
                    code = 'SH'
                elif 'rare' in label:
                    code = 'SR'
                elif 'state threatened' in label:
                    code = 'ST'
                elif 'threatened' in label:
                    code = 'T'

                if 'extremely rare' in label:
                    s_rank += 'S1'
                elif 'rare' in label:
                    s_rank += 'S2'
                if 'to rare' in label and 'extremely rare' not in label:
                    s_rank += 'S2'
                if 'uncommon' in label:
                    s_rank += 'S3'
                if 'fairly widespread' in label:
                    s_rank += 'S4'
                elif 'widespread' in label:
                    s_rank += 'S5'
                if 'historical' in label:
                    s_rank += 'SH'
                elif 'not applicable' in label:
                    s_rank += 'SNA'
                elif 'unranked' in label:
                    s_rank += 'SNR'
                elif 'unrankable' in label:
                    s_rank += 'SU'
                elif 'extirpated' in label:
                    s_rank += 'SX'
                if 'uncertain' in label:
                    s_rank += '?'

                if code:
                    c_status.endangerment_code = code
                if s_rank:
                    c_status.s_rank = s_rank
                if code or s_rank:
                    c_status.save()

        importer = Importer()
        for dist in orm['core.Distribution'].objects.all():
            status = dist.status
            if status:
                status = status.lower()
                present, native = importer._parse_status(status)
                dist.present = present
                dist.native = native
                dist.save()

        for image in orm['core.ImageType'].objects.all():
            if image.code == 'fl':
                code = image.name[:2]
                if image.name == 'root':
                    code = 'rt'
                if image.name == 'plant form':
                    code = 'pf'
                image.code = code
                image.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        for c_status in orm['core.ConservationStatus'].objects.all():
            if c_status.label:
                continue
            code = c_status.endangerment_code
            s_rank = c_status.s_rank
            label = []
            if code:
                l = endangerment_code_label(code)
                if l:
                    label.append(l)
            if s_rank:
                l = s_rank_label(s_rank)
                if l:
                    label.append()
            c_status.label = ','.join(label)
            c_status.save()

        for dist in orm['core.Distribution'].objects.all():
            if dist.status:
                continue
            present = dist.present
            native = dist.native
            status = 'absent'
            if present and native:
                status = 'present and native'
            elif present:
                status = 'present'
            dist.status = status
            dist.save()

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.character': {
            'Meta': {'ordering': "['short_name']", 'object_name': 'Character'},
            'character_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CharacterGroup']"}),
            'ease_of_observability': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hint': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'characters'", 'null': 'True', 'to': u"orm['core.Pile']"}),
            'question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'value_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'core.charactergroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'CharacterGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.charactervalue': {
            'Meta': {'object_name': 'CharacterValue'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'character_values'", 'to': u"orm['core.Character']"}),
            'friendly_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'value_flt': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_str': ('django.db.models.fields.CharField', [], {'max_length': '260', 'null': 'True', 'blank': 'True'})
        },
        u'core.commonname': {
            'Meta': {'ordering': "['common_name']", 'object_name': 'CommonName'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'common_names'", 'to': u"orm['core.Taxon']"})
        },
        u'core.conservationstatus': {
            'Meta': {'ordering': "('taxon', 'variety_subspecies_hybrid', 'region')", 'object_name': 'ConservationStatus'},
            'allow_public_posting': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'endangerment_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            's_rank': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conservation_statuses'", 'to': u"orm['core.Taxon']"}),
            'variety_subspecies_hybrid': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'core.contentimage': {
            'Meta': {'object_name': 'ContentImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '300'}),
            'image_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ImageType']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'core.copyrightholder': {
            'Meta': {'object_name': 'CopyrightHolder'},
            'coded_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'contact_info': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'date_record': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'expanded_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'permission_level': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'permission_location': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'permission_source': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'primary_bds': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'core.defaultfilter': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('key', 'pile', 'character'),)", 'object_name': 'DefaultFilter'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Character']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'pile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pile']"})
        },
        u'core.distribution': {
            'Meta': {'ordering': "('scientific_name', 'state', 'county')", 'object_name': 'Distribution'},
            'county': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'species_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'subspecific_epithet': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'})            
        },
        u'core.edit': {
            'Meta': {'object_name': 'Edit'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'coordinate1': ('django.db.models.fields.TextField', [], {}),
            'coordinate2': ('django.db.models.fields.TextField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemtype': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'old_value': ('django.db.models.fields.TextField', [], {})
        },
        u'core.family': {
            'Meta': {'ordering': "['name']", 'object_name': 'Family'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.genus': {
            'Meta': {'ordering': "['name']", 'object_name': 'Genus'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'genera'", 'to': u"orm['core.Family']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.glossaryterm': {
            'Meta': {'unique_together': "(('term', 'lay_definition'),)", 'object_name': 'GlossaryTerm'},
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lay_definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'core.goorchidtaxon': {
            'Meta': {'ordering': "['scientific_name']", 'object_name': 'GoOrchidTaxon', '_ormbases': [u'core.Taxon']},
            'ca_rank': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'flowering_phenology': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'global_rank': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'monitoring': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'mycorrhiza': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'pollination': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'propagation': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'ready_for_display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restoration': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            u'taxon_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Taxon']", 'unique': 'True', 'primary_key': 'True'}),
            'us_status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'core.homepageimage': {
            'Meta': {'ordering': "['partner_site', 'image']", 'object_name': 'HomePageImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'partner_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_page_images'", 'to': u"orm['core.PartnerSite']"})
        },
        u'core.imagetype': {
            'Meta': {'object_name': 'ImageType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.importlog': {
            'Meta': {'object_name': 'ImportLog'},
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'success': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.invasivestatus': {
            'Meta': {'ordering': "('taxon', 'region')", 'object_name': 'InvasiveStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invasive_in_region': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'prohibited_from_sale': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invasive_statuses'", 'to': u"orm['core.Taxon']"})
        },
        u'core.lookalike': {
            'Meta': {'object_name': 'Lookalike'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lookalike_characteristic': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'lookalike_scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lookalikes'", 'to': u"orm['core.Taxon']"})
        },
        u'core.parameter': {
            'Meta': {'ordering': "['name']", 'object_name': 'Parameter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.partnersite': {
            'Meta': {'ordering': "['short_name']", 'object_name': 'PartnerSite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'species': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Taxon']", 'through': u"orm['core.PartnerSpecies']", 'symmetrical': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        u'core.partnerspecies': {
            'Meta': {'unique_together': "(('species', 'partner'),)", 'object_name': 'PartnerSpecies'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.PartnerSite']"}),
            'simple_key': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Taxon']"}),
            'species_page_blurb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'species_page_heading': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'core.pile': {
            'Meta': {'ordering': "['name']", 'object_name': 'Pile'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'friendly_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_characteristics': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'notable_exceptions': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'pilegroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'piles'", 'null': 'True', 'to': u"orm['core.PileGroup']"}),
            'plant_preview_characters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'preview_characters'", 'symmetrical': 'False', 'through': u"orm['core.PlantPreviewCharacter']", 'to': u"orm['core.Character']"}),
            'sample_species_images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sample_for_piles'", 'symmetrical': 'False', 'through': u"orm['core.PileImage']", 'to': u"orm['core.ContentImage']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'species': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': u"orm['core.Taxon']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Video']", 'null': 'True'})
        },
        u'core.pilegroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'PileGroup'},
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'friendly_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_characteristics': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'notable_exceptions': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'sample_species_images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sample_for_pilegroups'", 'symmetrical': 'False', 'through': u"orm['core.PileGroupImage']", 'to': u"orm['core.ContentImage']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Video']", 'null': 'True'})
        },
        u'core.pilegroupimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'PileGroupImage'},
            'content_image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ContentImage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pile_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.PileGroup']"})
        },
        u'core.pileimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'PileImage'},
            'content_image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ContentImage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pile']"})
        },
        u'core.plantpreviewcharacter': {
            'Meta': {'ordering': "('partner_site', 'order')", 'unique_together': "(('pile', 'character', 'partner_site'),)", 'object_name': 'PlantPreviewCharacter'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Character']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'partner_site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.PartnerSite']", 'null': 'True', 'blank': 'True'}),
            'pile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pile']"})
        },
        u'core.regionalconservationstatus': {
            'Meta': {'ordering': "('region', 'status', 'rank')", 'unique_together': "(('taxon', 'region', 'status'), ('taxon', 'region', 'rank'))", 'object_name': 'RegionalConservationStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regional_conservation_statuses'", 'to': u"orm['core.GoOrchidTaxon']"}),
            'wetland_status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'core.sourcecitation': {
            'Meta': {'ordering': "['citation_text']", 'object_name': 'SourceCitation'},
            'article_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'citation_text': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'publication_year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publisher_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'publisher_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'core.synonym': {
            'Meta': {'ordering': "['scientific_name']", 'object_name': 'Synonym'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonyms'", 'to': u"orm['core.Taxon']"})
        },
        u'core.taxon': {
            'Meta': {'ordering': "['scientific_name']", 'object_name': 'Taxon'},
            'character_values': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.CharacterValue']", 'through': u"orm['core.TaxonCharacterValue']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'factoid': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxa'", 'to': u"orm['core.Family']"}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxa'", 'to': u"orm['core.Genus']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'north_american_introduced': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'north_american_native': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'piles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': u"orm['core.Pile']"}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'taxonomic_authority': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'variety_notes': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'wetland_indicator_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'core.taxoncharactervalue': {
            'Meta': {'unique_together': "(('taxon', 'character_value'),)", 'object_name': 'TaxonCharacterValue'},
            'character_value': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxon_character_values'", 'to': u"orm['core.CharacterValue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'literary_source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxon_character_values'", 'null': 'True', 'to': u"orm['core.SourceCitation']"}),
            'lit_source': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Taxon']"})
        },
        u'core.video': {
            'Meta': {'object_name': 'Video'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'youtube_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'core.wetlandindicator': {
            'Meta': {'ordering': "['sequence']", 'object_name': 'WetlandIndicator'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'friendly_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']
    symmetrical = True

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GoOrchidTaxon.ready_for_display'
        db.add_column('core_goorchidtaxon', 'ready_for_display',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GoOrchidTaxon.ready_for_display'
        db.delete_column('core_goorchidtaxon', 'ready_for_display')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.character': {
            'Meta': {'ordering': "['short_name']", 'object_name': 'Character'},
            'character_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.CharacterGroup']"}),
            'ease_of_observability': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hint': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'characters'", 'null': 'True', 'to': "orm['core.Pile']"}),
            'question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'value_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'core.charactergroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'CharacterGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'core.charactervalue': {
            'Meta': {'object_name': 'CharacterValue'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'character_values'", 'to': "orm['core.Character']"}),
            'friendly_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'value_flt': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_str': ('django.db.models.fields.CharField', [], {'max_length': '260', 'null': 'True', 'blank': 'True'})
        },
        'core.commonname': {
            'Meta': {'ordering': "['common_name']", 'object_name': 'CommonName'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'common_names'", 'to': "orm['core.Taxon']"})
        },
        'core.conservationstatus': {
            'Meta': {'ordering': "('region', 'label')", 'unique_together': "(('taxon', 'region', 'label'),)", 'object_name': 'ConservationStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conservation_statuses'", 'to': "orm['core.Taxon']"})
        },
        'core.contentimage': {
            'Meta': {'object_name': 'ContentImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '300'}),
            'image_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ImageType']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'core.copyrightholder': {
            'Meta': {'object_name': 'CopyrightHolder'},
            'coded_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'expanded_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'core.defaultfilter': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('key', 'pile', 'character'),)", 'object_name': 'DefaultFilter'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Character']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'pile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Pile']"})
        },
        'core.distribution': {
            'Meta': {'object_name': 'Distribution'},
            'county': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.edit': {
            'Meta': {'object_name': 'Edit'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'coordinate1': ('django.db.models.fields.TextField', [], {}),
            'coordinate2': ('django.db.models.fields.TextField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemtype': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'old_value': ('django.db.models.fields.TextField', [], {})
        },
        'core.family': {
            'Meta': {'ordering': "['name']", 'object_name': 'Family'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'core.genus': {
            'Meta': {'ordering': "['name']", 'object_name': 'Genus'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'genera'", 'to': "orm['core.Family']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'core.glossaryterm': {
            'Meta': {'unique_together': "(('term', 'lay_definition'),)", 'object_name': 'GlossaryTerm'},
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lay_definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'core.goorchidtaxon': {
            'Meta': {'ordering': "['scientific_name']", 'object_name': 'GoOrchidTaxon', '_ormbases': ['core.Taxon']},
            'ca_rank': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'flowering_phenology': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'global_rank': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'monitoring': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'mycorrhiza': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'pollination': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'propagation': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'ready_for_display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'restoration': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'taxon_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Taxon']", 'unique': 'True', 'primary_key': 'True'}),
            'us_status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'core.homepageimage': {
            'Meta': {'ordering': "['image']", 'object_name': 'HomePageImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'core.imagetype': {
            'Meta': {'object_name': 'ImageType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'core.lookalike': {
            'Meta': {'object_name': 'Lookalike'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lookalike_characteristic': ('django.db.models.fields.CharField', [], {'max_length': '900'}),
            'lookalike_scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lookalikes'", 'to': "orm['core.Taxon']"})
        },
        'core.parameter': {
            'Meta': {'ordering': "['name']", 'object_name': 'Parameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'core.partnersite': {
            'Meta': {'ordering': "['short_name']", 'object_name': 'PartnerSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'species': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Taxon']", 'through': "orm['core.PartnerSpecies']", 'symmetrical': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'core.partnerspecies': {
            'Meta': {'unique_together': "(('species', 'partner'),)", 'object_name': 'PartnerSpecies'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PartnerSite']"}),
            'simple_key': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Taxon']"}),
            'species_page_blurb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'species_page_heading': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'core.pile': {
            'Meta': {'ordering': "['name']", 'object_name': 'Pile'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'friendly_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_characteristics': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'notable_exceptions': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'pilegroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'piles'", 'null': 'True', 'to': "orm['core.PileGroup']"}),
            'plant_preview_characters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'preview_characters'", 'symmetrical': 'False', 'through': "orm['core.PlantPreviewCharacter']", 'to': "orm['core.Character']"}),
            'sample_species_images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sample_for_piles'", 'symmetrical': 'False', 'through': "orm['core.PileImage']", 'to': "orm['core.ContentImage']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'species': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['core.Taxon']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Video']", 'null': 'True'})
        },
        'core.pilegroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'PileGroup'},
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'friendly_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_characteristics': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'notable_exceptions': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'sample_species_images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sample_for_pilegroups'", 'symmetrical': 'False', 'through': "orm['core.PileGroupImage']", 'to': "orm['core.ContentImage']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Video']", 'null': 'True'})
        },
        'core.pilegroupimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'PileGroupImage'},
            'content_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ContentImage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pile_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PileGroup']"})
        },
        'core.pileimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'PileImage'},
            'content_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ContentImage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Pile']"})
        },
        'core.plantpreviewcharacter': {
            'Meta': {'ordering': "('partner_site', 'order')", 'unique_together': "(('pile', 'character', 'partner_site'),)", 'object_name': 'PlantPreviewCharacter'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'partner_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PartnerSite']", 'null': 'True', 'blank': 'True'}),
            'pile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Pile']"})
        },
        'core.regionalconservationstatus': {
            'Meta': {'ordering': "('region', 'status', 'rank')", 'unique_together': "(('taxon', 'region', 'status'), ('taxon', 'region', 'rank'))", 'object_name': 'RegionalConservationStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regional_conservation_statuses'", 'to': "orm['core.GoOrchidTaxon']"})
        },
        'core.synonym': {
            'Meta': {'ordering': "['scientific_name']", 'object_name': 'Synonym'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonyms'", 'to': "orm['core.Taxon']"})
        },
        'core.taxon': {
            'Meta': {'ordering': "['scientific_name']", 'object_name': 'Taxon'},
            'character_values': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.CharacterValue']", 'through': "orm['core.TaxonCharacterValue']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'factoid': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxa'", 'to': "orm['core.Family']"}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxa'", 'to': "orm['core.Genus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'north_american_introduced': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'north_american_native': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'piles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': "orm['core.Pile']"}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'taxonomic_authority': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'variety_notes': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'wetland_indicator_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'core.taxoncharactervalue': {
            'Meta': {'unique_together': "(('taxon', 'character_value'),)", 'object_name': 'TaxonCharacterValue'},
            'character_value': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxon_character_values'", 'to': "orm['core.CharacterValue']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lit_source': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Taxon']"})
        },
        'core.video': {
            'Meta': {'object_name': 'Video'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'youtube_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'core.wetlandindicator': {
            'Meta': {'ordering': "['sequence']", 'object_name': 'WetlandIndicator'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'friendly_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']
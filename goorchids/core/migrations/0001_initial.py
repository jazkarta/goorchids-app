# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Parameter'
        db.create_table('core_parameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['Parameter'])

        # Adding model 'CharacterGroup'
        db.create_table('core_charactergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('core', ['CharacterGroup'])

        # Adding model 'GlossaryTerm'
        db.create_table('core_glossaryterm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lay_definition', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('highlight', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['GlossaryTerm'])

        # Adding unique constraint on 'GlossaryTerm', fields ['term', 'lay_definition']
        db.create_unique('core_glossaryterm', ['term', 'lay_definition'])

        # Adding model 'Character'
        db.create_table('core_character', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('character_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CharacterGroup'])),
            ('pile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='characters', null=True, to=orm['core.Pile'])),
            ('ease_of_observability', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('value_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('hint', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Character'])

        # Adding model 'CharacterValue'
        db.create_table('core_charactervalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value_str', self.gf('django.db.models.fields.CharField')(max_length=260, null=True, blank=True)),
            ('value_min', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('value_max', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('value_flt', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(related_name='character_values', to=orm['core.Character'])),
            ('friendly_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['CharacterValue'])

        # Adding model 'Pile'
        db.create_table('core_pile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('friendly_title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Video'], null=True)),
            ('key_characteristics', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('notable_exceptions', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pilegroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='piles', null=True, to=orm['core.PileGroup'])),
        ))
        db.send_create_signal('core', ['Pile'])

        # Adding M2M table for field species on 'Pile'
        db.create_table('core_pile_species', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pile', models.ForeignKey(orm['core.pile'], null=False)),
            ('taxon', models.ForeignKey(orm['core.taxon'], null=False))
        ))
        db.create_unique('core_pile_species', ['pile_id', 'taxon_id'])

        # Adding model 'PileImage'
        db.create_table('core_pileimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ContentImage'])),
            ('pile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Pile'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('core', ['PileImage'])

        # Adding model 'PileGroup'
        db.create_table('core_pilegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('friendly_title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Video'], null=True)),
            ('key_characteristics', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('notable_exceptions', self.gf('tinymce.models.HTMLField')(blank=True)),
        ))
        db.send_create_signal('core', ['PileGroup'])

        # Adding model 'PileGroupImage'
        db.create_table('core_pilegroupimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ContentImage'])),
            ('pile_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PileGroup'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('core', ['PileGroupImage'])

        # Adding model 'ImageType'
        db.create_table('core_imagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('core', ['ImageType'])

        # Adding model 'ContentImage'
        db.create_table('core_contentimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=300)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('rank', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ImageType'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('core', ['ContentImage'])

        # Adding model 'HomePageImage'
        db.create_table('core_homepageimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('core', ['HomePageImage'])

        # Adding model 'Family'
        db.create_table('core_family', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('core', ['Family'])

        # Adding model 'Genus'
        db.create_table('core_genus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(related_name='genera', to=orm['core.Family'])),
        ))
        db.send_create_signal('core', ['Genus'])

        # Adding model 'Synonym'
        db.create_table('core_synonym', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scientific_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(related_name='synonyms', to=orm['core.Taxon'])),
        ))
        db.send_create_signal('core', ['Synonym'])

        # Adding model 'CommonName'
        db.create_table('core_commonname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(related_name='common_names', to=orm['core.Taxon'])),
        ))
        db.send_create_signal('core', ['CommonName'])

        # Adding model 'Lookalike'
        db.create_table('core_lookalike', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lookalike_scientific_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lookalike_characteristic', self.gf('django.db.models.fields.CharField')(max_length=900)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lookalikes', to=orm['core.Taxon'])),
        ))
        db.send_create_signal('core', ['Lookalike'])

        # Adding model 'WetlandIndicator'
        db.create_table('core_wetlandindicator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('friendly_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['WetlandIndicator'])

        # Adding model 'Taxon'
        db.create_table('core_taxon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scientific_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taxa', to=orm['core.Family'])),
            ('genus', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taxa', to=orm['core.Genus'])),
            ('taxonomic_authority', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('factoid', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('wetland_indicator_code', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('north_american_native', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('north_american_introduced', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('variety_notes', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal('core', ['Taxon'])

        # Adding model 'TaxonCharacterValue'
        db.create_table('core_taxoncharactervalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Taxon'])),
            ('character_value', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taxon_character_values', to=orm['core.CharacterValue'])),
            ('lit_source', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['TaxonCharacterValue'])

        # Adding unique constraint on 'TaxonCharacterValue', fields ['taxon', 'character_value']
        db.create_unique('core_taxoncharactervalue', ['taxon_id', 'character_value_id'])

        # Adding model 'Edit'
        db.create_table('core_edit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.TextField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('itemtype', self.gf('django.db.models.fields.TextField')(db_index=True)),
            ('coordinate1', self.gf('django.db.models.fields.TextField')()),
            ('coordinate2', self.gf('django.db.models.fields.TextField')()),
            ('old_value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['Edit'])

        # Adding model 'ConservationStatus'
        db.create_table('core_conservationstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(related_name='conservation_statuses', to=orm['core.Taxon'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('core', ['ConservationStatus'])

        # Adding unique constraint on 'ConservationStatus', fields ['taxon', 'region', 'label']
        db.create_unique('core_conservationstatus', ['taxon_id', 'region', 'label'])

        # Adding model 'DefaultFilter'
        db.create_table('core_defaultfilter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('pile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Pile'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Character'], null=True)),
        ))
        db.send_create_signal('core', ['DefaultFilter'])

        # Adding unique constraint on 'DefaultFilter', fields ['key', 'pile', 'character']
        db.create_unique('core_defaultfilter', ['key', 'pile_id', 'character_id'])

        # Adding model 'PartnerSite'
        db.create_table('core_partnersite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('core', ['PartnerSite'])

        # Adding M2M table for field users on 'PartnerSite'
        db.create_table('core_partnersite_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partnersite', models.ForeignKey(orm['core.partnersite'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('core_partnersite_users', ['partnersite_id', 'user_id'])

        # Adding model 'PartnerSpecies'
        db.create_table('core_partnerspecies', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Taxon'])),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PartnerSite'])),
            ('simple_key', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('species_page_heading', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('species_page_blurb', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['PartnerSpecies'])

        # Adding unique constraint on 'PartnerSpecies', fields ['species', 'partner']
        db.create_unique('core_partnerspecies', ['species_id', 'partner_id'])

        # Adding model 'PlantPreviewCharacter'
        db.create_table('core_plantpreviewcharacter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Pile'])),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Character'])),
            ('partner_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PartnerSite'], null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['PlantPreviewCharacter'])

        # Adding unique constraint on 'PlantPreviewCharacter', fields ['pile', 'character', 'partner_site']
        db.create_unique('core_plantpreviewcharacter', ['pile_id', 'character_id', 'partner_site_id'])

        # Adding model 'Distribution'
        db.create_table('core_distribution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scientific_name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Distribution'])

        # Adding model 'CopyrightHolder'
        db.create_table('core_copyrightholder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coded_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('expanded_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('copyright', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('core', ['CopyrightHolder'])

        # Adding model 'Video'
        db.create_table('core_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('youtube_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('core', ['Video'])

        # Adding model 'GoOrchidTaxon'
        db.create_table('core_goorchidtaxon', (
            ('taxon_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Taxon'], unique=True, primary_key=True)),
            ('pollination', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('mycorrhiza', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('monitoring', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('propagation', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('restoration', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('flowering_phenology', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('global_rank', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('us_status', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('ca_rank', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['GoOrchidTaxon'])

        # Adding model 'RegionalConservationStatus'
        db.create_table('core_regionalconservationstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regional_conservation_statuses', to=orm['core.GoOrchidTaxon'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('core', ['RegionalConservationStatus'])

        # Adding unique constraint on 'RegionalConservationStatus', fields ['taxon', 'region', 'status']
        db.create_unique('core_regionalconservationstatus', ['taxon_id', 'region', 'status'])

        # Adding unique constraint on 'RegionalConservationStatus', fields ['taxon', 'region', 'rank']
        db.create_unique('core_regionalconservationstatus', ['taxon_id', 'region', 'rank'])


    def backwards(self, orm):
        # Removing unique constraint on 'RegionalConservationStatus', fields ['taxon', 'region', 'rank']
        db.delete_unique('core_regionalconservationstatus', ['taxon_id', 'region', 'rank'])

        # Removing unique constraint on 'RegionalConservationStatus', fields ['taxon', 'region', 'status']
        db.delete_unique('core_regionalconservationstatus', ['taxon_id', 'region', 'status'])

        # Removing unique constraint on 'PlantPreviewCharacter', fields ['pile', 'character', 'partner_site']
        db.delete_unique('core_plantpreviewcharacter', ['pile_id', 'character_id', 'partner_site_id'])

        # Removing unique constraint on 'PartnerSpecies', fields ['species', 'partner']
        db.delete_unique('core_partnerspecies', ['species_id', 'partner_id'])

        # Removing unique constraint on 'DefaultFilter', fields ['key', 'pile', 'character']
        db.delete_unique('core_defaultfilter', ['key', 'pile_id', 'character_id'])

        # Removing unique constraint on 'ConservationStatus', fields ['taxon', 'region', 'label']
        db.delete_unique('core_conservationstatus', ['taxon_id', 'region', 'label'])

        # Removing unique constraint on 'TaxonCharacterValue', fields ['taxon', 'character_value']
        db.delete_unique('core_taxoncharactervalue', ['taxon_id', 'character_value_id'])

        # Removing unique constraint on 'GlossaryTerm', fields ['term', 'lay_definition']
        db.delete_unique('core_glossaryterm', ['term', 'lay_definition'])

        # Deleting model 'Parameter'
        db.delete_table('core_parameter')

        # Deleting model 'CharacterGroup'
        db.delete_table('core_charactergroup')

        # Deleting model 'GlossaryTerm'
        db.delete_table('core_glossaryterm')

        # Deleting model 'Character'
        db.delete_table('core_character')

        # Deleting model 'CharacterValue'
        db.delete_table('core_charactervalue')

        # Deleting model 'Pile'
        db.delete_table('core_pile')

        # Removing M2M table for field species on 'Pile'
        db.delete_table('core_pile_species')

        # Deleting model 'PileImage'
        db.delete_table('core_pileimage')

        # Deleting model 'PileGroup'
        db.delete_table('core_pilegroup')

        # Deleting model 'PileGroupImage'
        db.delete_table('core_pilegroupimage')

        # Deleting model 'ImageType'
        db.delete_table('core_imagetype')

        # Deleting model 'ContentImage'
        db.delete_table('core_contentimage')

        # Deleting model 'HomePageImage'
        db.delete_table('core_homepageimage')

        # Deleting model 'Family'
        db.delete_table('core_family')

        # Deleting model 'Genus'
        db.delete_table('core_genus')

        # Deleting model 'Synonym'
        db.delete_table('core_synonym')

        # Deleting model 'CommonName'
        db.delete_table('core_commonname')

        # Deleting model 'Lookalike'
        db.delete_table('core_lookalike')

        # Deleting model 'WetlandIndicator'
        db.delete_table('core_wetlandindicator')

        # Deleting model 'Taxon'
        db.delete_table('core_taxon')

        # Removing M2M table for field piles on 'Taxon'
        db.delete_table('core_pile_species')

        # Deleting model 'TaxonCharacterValue'
        db.delete_table('core_taxoncharactervalue')

        # Deleting model 'Edit'
        db.delete_table('core_edit')

        # Deleting model 'ConservationStatus'
        db.delete_table('core_conservationstatus')

        # Deleting model 'DefaultFilter'
        db.delete_table('core_defaultfilter')

        # Deleting model 'PartnerSite'
        db.delete_table('core_partnersite')

        # Removing M2M table for field users on 'PartnerSite'
        db.delete_table('core_partnersite_users')

        # Deleting model 'PartnerSpecies'
        db.delete_table('core_partnerspecies')

        # Deleting model 'PlantPreviewCharacter'
        db.delete_table('core_plantpreviewcharacter')

        # Deleting model 'Distribution'
        db.delete_table('core_distribution')

        # Deleting model 'CopyrightHolder'
        db.delete_table('core_copyrightholder')

        # Deleting model 'Video'
        db.delete_table('core_video')

        # Deleting model 'GoOrchidTaxon'
        db.delete_table('core_goorchidtaxon')

        # Deleting model 'RegionalConservationStatus'
        db.delete_table('core_regionalconservationstatus')


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

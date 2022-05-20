# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    operations = [
        migrations.CreateModel(
            name='GoOrchidTaxon',
            fields=[
                ('taxon_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Taxon', on_delete=models.PROTECT)),
                ('ready_for_display', models.BooleanField(default=False)),
                ('pollination', models.CharField(max_length=1000, blank=True)),
                ('mycorrhiza', models.CharField(max_length=1000, blank=True)),
                ('monitoring', models.CharField(max_length=1000, blank=True)),
                ('propagation', models.CharField(max_length=1000, blank=True)),
                ('restoration', models.CharField(max_length=1000, blank=True)),
                ('flowering_phenology', models.CharField(max_length=1000, blank=True)),
                ('global_rank', models.CharField(blank=True, max_length=2, null=True, choices=[(b'GX', b'Presumed Extirpated'), (b'GH', b'Possible Extirpated'), (b'G1', b'Critically Imperiled'), (b'G2', b'Imperiled'), (b'G3', b'Vulnerable'), (b'G4', b'Apparently Secure'), (b'G5', b'Secure')])),
                ('us_status', models.CharField(blank=True, max_length=2, null=True, verbose_name=b'US status', choices=[(b'LE', b'Listed Endangered'), (b'LT', b'Listed Threatened'), (b'PE', b'Proposed Endangered'), (b'PT', b'Proposed Threatened'), (b'C', b'Candidate')])),
                ('ca_rank', models.CharField(blank=True, max_length=3, null=True, verbose_name=b'Canadian Status', choices=[(b'0.2', b'Extinct'), (b'0.1', b'Extirpated'), (b'1', b'At Risk'), (b'2', b'May Be At Risk'), (b'3', b'Sensitive'), (b'4', b'Secure'), (b'5', b'Undetermined'), (b'6', b'Not assessed'), (b'7', b'Exotic'), (b'8', b'Accidental'), (b'E', b'Endangered'), (b'T', b'Threatened'), (b'SC', b'Special Concern'), (b'C', b'Candidate')])),
            ],
            options={
                'db_table': 'core_goorchidtaxon',
                'verbose_name': 'taxon',
                'verbose_name_plural': 'taxa',
            },
            bases=('core.taxon',),
        ),
        migrations.CreateModel(
            name='ImportLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('start', models.DateTimeField()),
                ('duration', models.IntegerField(null=True)),
                ('success', models.NullBooleanField()),
                ('message', models.TextField(null=True)),
            ],
            options={
                'db_table': 'core_importlog',
            },
        ),
        migrations.CreateModel(
            name='RegionalConservationStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', models.CharField(max_length=80, choices=[(b'al', 'Alabama'), (b'ak', 'Alaska'), (b'ab', 'Alberta'), (b'az', 'Arizona'), (b'ar', 'Arkansas'), (b'bc', 'British Columbia'), (b'ca', 'California'), (b'co', 'Colorado'), (b'ct', 'Connecticut'), (b'de', 'Delaware'), (b'dc', 'District of Columbia'), (b'fl', 'Florida'), (b'ga', 'Georgia'), (b'hi', 'Hawaii'), (b'id', 'Idaho'), (b'il', 'Illinois'), (b'in', 'Indiana'), (b'ia', 'Iowa'), (b'ks', 'Kansas'), (b'ky', 'Kentucky'), (b'la', 'Louisiana'), (b'me', 'Maine'), (b'mb', 'Manitoba'), (b'md', 'Maryland'), (b'ma', 'Massachusetts'), (b'mi', 'Michigan'), (b'mn', 'Minnesota'), (b'ms', 'Mississippi'), (b'mo', 'Missouri'), (b'mt', 'Montana'), (b'ne', 'Nebraska'), (b'nv', 'Nevada'), (b'nb', 'New Brunswick'), (b'nh', 'New Hampshire'), (b'nj', 'New Jersey'), (b'nm', 'New Mexico'), (b'ny', 'New York'), (b'nl', 'Newfoundland and Labrador'), (b'nc', 'North Carolina'), (b'nd', 'North Dakota'), (b'nt', 'Northwest Territories'), (b'ns', 'Nova Scotia'), (b'nu', 'Nunavut'), (b'oh', 'Ohio'), (b'ok', 'Oklahoma'), (b'on', 'Ontario'), (b'or', 'Oregon'), (b'pa', 'Pennsylvania'), (b'pe', 'Prince Edward Island'), (b'qc', 'Quebec'), (b'ri', 'Rhode Island'), (b'sk', 'Saskatchewan'), (b'sc', 'South Carolina'), (b'sd', 'South Dakota'), (b'tn', 'Tennessee'), (b'tx', 'Texas'), (b'ut', 'Utah'), (b'vt', 'Vermont'), (b'va', 'Virginia'), (b'wa', 'Washington'), (b'wv', 'West Virginia'), (b'wi', 'Wisconsin'), (b'wy', 'Wyoming'), (b'yt', 'Yukon')])),
                ('status', models.CharField(default=None, max_length=2, null=True, blank=True, choices=[(b'E', b'Endangered'), (b'T', b'Threatened'), (b'X', b'Extirpated'), (b'SC', b'Species of Concern'), (b'H', b'Historical')])),
                ('rank', models.CharField(default=None, max_length=2, null=True, blank=True, choices=[(b'SX', b'Presumed Extirpated'), (b'SH', b'Possible Extirpated'), (b'S1', b'Highly State Rare'), (b'S2', b'State Rare'), (b'S3', b'Watch List'), (b'S4', b'Apparently Secure'), (b'S5', b'Secure')])),
                ('wetland_status', models.CharField(default=None, max_length=4, null=True, blank=True, choices=[(b'OBL', b'Obligate Wetland'), (b'FACW', b'Facultative Wetland'), (b'FAC', b'Facultative'), (b'FACU', b'Facultative Upland'), (b'UPL', b'Upland')])),
                ('taxon', models.ForeignKey(related_name='regional_conservation_statuses', to='goorchids_core.GoOrchidTaxon', on_delete=models.PROTECT)),
            ],
            options={
                'ordering': ('region', 'status', 'rank'),
                'db_table': 'core_regionalconservationstatus',
                'verbose_name_plural': 'regional conservation statuses',
            },
        ),
        migrations.AlterUniqueTogether(
            name='regionalconservationstatus',
            unique_together=set([('taxon', 'region', 'rank'), ('taxon', 'region', 'status')]),
        ),
    ]

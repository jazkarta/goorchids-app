# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

sql = """UPDATE django_content_type
         SET app_label = 'goordchids_core'
         WHERE (model = 'goorchidtaxon' OR model = 'regionalconservationstatus'
                OR model = 'importlog')
               AND app_label = 'core';"""

reverse_sql = """UPDATE django_content_type
                 SET app_label = 'core',
                     model = 'profile'
                 WHERE (model = 'goorchidtaxon' OR model = 'regionalconservationstatus'
                        OR model = 'importlog')
                       AND app_label = 'goorchids_core';"""


class Migration(migrations.Migration):

    dependencies = [
        ('goorchids_core', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(sql, reverse_sql)
    ]

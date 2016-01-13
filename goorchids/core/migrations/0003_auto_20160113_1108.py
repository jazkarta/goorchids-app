# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goorchids_core', '0002_migrate_ctypes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goorchidtaxon',
            name='pollination',
            field=models.CharField(max_length=2500, blank=True),
        ),
    ]

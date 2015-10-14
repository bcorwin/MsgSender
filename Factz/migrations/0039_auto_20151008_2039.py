# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0038_auto_20151008_2035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='send_base',
            new_name='send_start',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='send_delay',
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_end',
            field=models.TimeField(default=datetime.datetime(1, 1, 1, 23, 45)),
        ),
    ]

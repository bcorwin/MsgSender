# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0013_auto_20150914_1439'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variable',
            old_name='value',
            new_name='val',
        ),
    ]

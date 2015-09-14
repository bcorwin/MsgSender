# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0012_auto_20150911_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

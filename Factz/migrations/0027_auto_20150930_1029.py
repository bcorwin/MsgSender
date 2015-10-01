# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0026_auto_20150930_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='follow_up',
            field=models.CharField(max_length=160, default='This field is blank'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='source',
            field=models.CharField(max_length=160, default='This filed is blank'),
            preserve_default=False,
        ),
    ]

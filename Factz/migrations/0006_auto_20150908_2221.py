# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0005_auto_20150908_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='last_sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='number',
            name='last_sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='last_sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

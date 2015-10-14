# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0043_auto_20151013_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentmessage',
            name='followup_code',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='message_code',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='followup_status',
            field=models.CharField(max_length=64, blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='message_status',
            field=models.CharField(max_length=64, blank=True, default=None, null=True),
        ),
    ]

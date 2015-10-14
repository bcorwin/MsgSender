# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0041_remove_subscription_last_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentmessage',
            name='attempted',
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='followup_code',
            field=models.IntegerField(blank=True, null=True, default=None),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='followup_status',
            field=models.CharField(max_length=64, blank=True, null=True, default=None),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='message_code',
            field=models.IntegerField(blank=True, null=True, default=None),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='message_status',
            field=models.CharField(max_length=64, blank=True, null=True, default=None),
        ),
    ]

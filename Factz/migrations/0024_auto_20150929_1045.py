# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0023_subscription_sent_message_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sentmessage',
            old_name='actual_time',
            new_name='actual_end',
        ),
        migrations.RenameField(
            model_name='sentmessage',
            old_name='scheduled_time',
            new_name='scheduled_start',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='sent_message_id',
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='actual_run',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='actual_start',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

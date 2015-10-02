# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0029_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activesubscription',
            old_name='message_cnt',
            new_name='count',
        ),
        migrations.RenameField(
            model_name='activesubscription',
            old_name='message',
            new_name='last_message',
        ),
        migrations.RenameField(
            model_name='number',
            old_name='message_cnt',
            new_name='count',
        ),
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
            model_name='activesubscription',
            name='fu_fail',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='fu_na',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='fu_success',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='msg_fail',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='msg_na',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='msg_success',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='next_send',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='run_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_end',
            field=models.TimeField(default=datetime.datetime(1, 1, 1, 23, 45)),
        ),
    ]

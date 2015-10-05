# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0029_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='dailySend',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('next_send_date', models.DateField(default=datetime.datetime(2000, 1, 1, 0, 0))),
            ],
        ),
        migrations.RemoveField(
            model_name='activesubscription',
            name='message_cnt',
        ),
        migrations.RemoveField(
            model_name='message',
            name='count',
        ),
        migrations.RemoveField(
            model_name='number',
            name='message_cnt',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='actual_end',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='actual_run',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='actual_start',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='fu_fail',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='fu_na',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='fu_success',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='msg_fail',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='msg_na',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='msg_success',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='scheduled_start',
        ),
        migrations.RemoveField(
            model_name='sentmessage',
            name='subscription',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='count',
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='active_subscription',
            field=models.ForeignKey(to='Factz.activeSubscription', null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='attempted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='next_send',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='next_send_date',
            field=models.DateField(default=datetime.datetime(2000, 1, 1, 0, 0)),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='sent_time',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='message',
            field=models.ForeignKey(to='Factz.Message', null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='dailysend',
            name='message',
            field=models.ForeignKey(to='Factz.Message'),
        ),
        migrations.AddField(
            model_name='dailysend',
            name='subscription',
            field=models.ForeignKey(to='Factz.Subscription'),
        ),
    ]

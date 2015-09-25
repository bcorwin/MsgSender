# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0019_subscription_next_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='send_base',
            field=models.TimeField(default=datetime.datetime(1, 1, 1, 16, 0)),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_delay',
            field=models.PositiveIntegerField(default=465),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_friday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_monday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_saturday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_sunday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_thursday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_tuesday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_wednesday',
            field=models.BooleanField(default=True),
        ),
    ]

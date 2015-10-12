# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0039_auto_20151008_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysend',
            name='next_send',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='daily_send',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='Factz.dailySend'),
        ),
    ]

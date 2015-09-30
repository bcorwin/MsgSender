# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0025_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentmessage',
            name='fail_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='na_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='success_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activesubscription',
            name='message',
            field=models.ForeignKey(to='Factz.Message', on_delete=django.db.models.deletion.PROTECT, blank=True, default=None, null=True),
        ),
    ]

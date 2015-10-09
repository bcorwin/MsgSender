# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0030_auto_20151005_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessage',
            name='active_subscription',
            field=models.ForeignKey(null=True, to='Factz.activeSubscription', blank=True, on_delete=django.db.models.deletion.PROTECT, default=None),
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='message',
            field=models.ForeignKey(null=True, to='Factz.Message', blank=True, on_delete=django.db.models.deletion.PROTECT, default=None),
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='next_send',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='next_send_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='sent_time',
            field=models.DateTimeField(),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0026_auto_20150930_0931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sentmessage',
            old_name='fail_count',
            new_name='msg_fail',
        ),
        migrations.RenameField(
            model_name='sentmessage',
            old_name='na_count',
            new_name='msg_na',
        ),
        migrations.RenameField(
            model_name='sentmessage',
            old_name='success_count',
            new_name='msg_success',
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='fu_fail',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='fu_na',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='fu_success',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

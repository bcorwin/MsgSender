# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0021_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='sentMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scheduled_time', models.DateTimeField(null=True, blank=True)),
                ('actual_time', models.DateTimeField(null=True, blank=True)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='Factz.Message', null=True)),
            ],
        ),
    ]

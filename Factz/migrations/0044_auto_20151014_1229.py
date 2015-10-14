# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0043_sentmessage_attempted'),
    ]

    operations = [
        migrations.CreateModel(
            name='customMessage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('message', models.CharField(max_length=160)),
                ('last_sent', models.DateTimeField(null=True, blank=True)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='custom_message',
            field=models.ForeignKey(null=True, to='Factz.customMessage', on_delete=django.db.models.deletion.PROTECT, blank=True, default=None),
        ),
    ]

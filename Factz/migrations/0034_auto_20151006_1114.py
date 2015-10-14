# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0033_auto_20151006_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='message',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='number',
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='rating',
            field=models.IntegerField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], default=None),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]

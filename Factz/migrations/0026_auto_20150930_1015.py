# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0025_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='number',
            name='email',
            field=models.CharField(max_length=32, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='number',
            name='name',
            field=models.CharField(max_length=32, blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0016_auto_20150918_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]

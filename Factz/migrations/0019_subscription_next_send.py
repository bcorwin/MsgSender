# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0018_auto_20150923_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='next_send',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

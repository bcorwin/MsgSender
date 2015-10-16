# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0046_auto_20151015_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='custommessage',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unconfirmed',
            name='phone_number',
            field=models.CharField(default='NULL', max_length=15),
            preserve_default=False,
        ),
    ]

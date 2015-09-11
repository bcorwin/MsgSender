# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Factz.models


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0002_unconfirmed_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='unconfirmed',
            name='confirmation_code',
            field=models.CharField(default=Factz.models.rand_code, max_length=6),
        ),
    ]

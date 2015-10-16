# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0044_auto_20151014_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentmessage',
            name='is_custom',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

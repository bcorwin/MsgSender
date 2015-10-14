# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0037_auto_20151008_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessage',
            name='next_send',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0031_auto_20151006_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysend',
            name='next_send_date',
            field=models.DateField(),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0032_auto_20151006_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessage',
            name='sent_time',
            field=models.DateTimeField(null=True, blank=True, default=None),
        ),
    ]

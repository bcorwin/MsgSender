# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0042_auto_20151013_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentmessage',
            name='attempted',
            field=models.IntegerField(choices=[(0, 'Not attempted'), (1, 'Message attempted'), (2, 'Completed')], default=0),
        ),
    ]

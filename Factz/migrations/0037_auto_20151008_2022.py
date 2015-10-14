# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0036_auto_20151008_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysend',
            name='message',
            field=models.ForeignKey(blank=True, to='Factz.Message', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0035_auto_20151006_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysend',
            name='message',
            field=models.ForeignKey(to='Factz.Message', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0006_auto_20150908_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='message_id',
            field=models.ForeignKey(blank=True, to='Factz.Message', null=True),
        ),
    ]

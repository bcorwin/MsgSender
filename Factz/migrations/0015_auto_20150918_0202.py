# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0014_auto_20150914_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activesubscription',
            name='message_id',
            field=models.ForeignKey(default=None, blank=True, to='Factz.Message', null=True),
        ),
    ]

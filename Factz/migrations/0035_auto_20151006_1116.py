# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0034_auto_20151006_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activesubscription',
            name='last_sent',
            field=models.DateTimeField(null=True, default=None, blank=True),
        ),
    ]

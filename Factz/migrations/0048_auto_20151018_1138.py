# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0047_custommessage_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessage',
            name='next_send',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

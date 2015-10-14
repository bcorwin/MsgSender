# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0040_auto_20151009_0802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='last_sent',
        ),
    ]

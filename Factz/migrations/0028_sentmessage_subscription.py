# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0027_auto_20150930_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentmessage',
            name='subscription',
            field=models.ForeignKey(to='Factz.Subscription', on_delete=django.db.models.deletion.PROTECT, default=1),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0045_sentmessage_is_custom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessage',
            name='active_subscription',
            field=models.ForeignKey(default=None, to='Factz.activeSubscription', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='next_send',
            field=models.DateTimeField(),
        ),
    ]

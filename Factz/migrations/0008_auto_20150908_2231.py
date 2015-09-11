# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0007_auto_20150908_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='message_id',
        ),
        migrations.AddField(
            model_name='message',
            name='subscription_id',
            field=models.ForeignKey(default=1, to='Factz.Subscription'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0022_sentmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='sent_message_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]

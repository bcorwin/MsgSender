# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0015_auto_20150918_0202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activesubscription',
            old_name='message_id',
            new_name='message',
        ),
        migrations.RenameField(
            model_name='activesubscription',
            old_name='number_id',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='activesubscription',
            old_name='subscription_id',
            new_name='subscription',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='subscription_id',
            new_name='subscription',
        ),
        migrations.AlterUniqueTogether(
            name='activesubscription',
            unique_together=set([('number', 'subscription')]),
        ),
    ]

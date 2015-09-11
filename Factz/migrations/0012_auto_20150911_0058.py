# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0011_auto_20150909_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='activesubscription',
            name='message_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='message_id',
            field=models.ForeignKey(default=-1, to='Factz.Message'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='activesubscription',
            unique_together=set([('number_id', 'subscription_id')]),
        ),
    ]

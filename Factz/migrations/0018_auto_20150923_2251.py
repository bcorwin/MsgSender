# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0017_subscription_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activesubscription',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='Factz.Message', null=True),
        ),
        migrations.AlterField(
            model_name='activesubscription',
            name='number',
            field=models.ForeignKey(to='Factz.Number', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='activesubscription',
            name='subscription',
            field=models.ForeignKey(to='Factz.Subscription', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='message',
            name='subscription',
            field=models.ForeignKey(to='Factz.Subscription', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]

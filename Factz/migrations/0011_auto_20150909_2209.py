# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Factz.models


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0010_auto_20150909_0009'),
    ]

    operations = [
        migrations.CreateModel(
            name='activeSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('last_sent', models.DateTimeField(null=True, blank=True)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='unconfirmed',
            name='subscription_id',
        ),
        migrations.RemoveField(
            model_name='number',
            name='active',
        ),
        migrations.RemoveField(
            model_name='number',
            name='subscription_id',
        ),
        migrations.AddField(
            model_name='number',
            name='confirmation_code',
            field=models.CharField(default=Factz.models.rand_code, max_length=6),
        ),
        migrations.AddField(
            model_name='number',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Unconfirmed',
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='number_id',
            field=models.ForeignKey(to='Factz.Number'),
        ),
        migrations.AddField(
            model_name='activesubscription',
            name='subscription_id',
            field=models.ForeignKey(to='Factz.Subscription'),
        ),
    ]

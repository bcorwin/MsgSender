# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0009_auto_20150909_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='inserted_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='last_sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='number',
            name='inserted_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='number',
            name='last_sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='number',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='inserted_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='last_sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='unconfirmed',
            name='inserted_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

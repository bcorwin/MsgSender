# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0008_auto_20150908_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='follow_up',
            field=models.CharField(max_length=160, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='inserted_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='last_sent',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='source',
            field=models.CharField(max_length=160, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='updated_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='number',
            name='inserted_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='number',
            name='last_sent',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='number',
            name='updated_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='inserted_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='last_sent',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='updated_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='unconfirmed',
            name='inserted_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

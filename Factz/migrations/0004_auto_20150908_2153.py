# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0003_unconfirmed_confirmation_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=320)),
                ('follow_up', models.CharField(max_length=160)),
                ('source', models.CharField(max_length=160)),
                ('count', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('last_sent', models.DateTimeField(blank=True)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Numbers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('message_cnt', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('last_sent', models.DateTimeField(blank=True)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=16)),
                ('active', models.BooleanField()),
                ('last_sent', models.DateTimeField(blank=True)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('message_id', models.ForeignKey(to='Factz.Messages')),
            ],
        ),
        migrations.CreateModel(
            name='Variables',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('value', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='numbers',
            name='subscription_id',
            field=models.ForeignKey(to='Factz.Subscriptions'),
        ),
        migrations.AddField(
            model_name='unconfirmed',
            name='subscription_id',
            field=models.ForeignKey(default=-1, to='Factz.Subscriptions'),
            preserve_default=False,
        ),
    ]

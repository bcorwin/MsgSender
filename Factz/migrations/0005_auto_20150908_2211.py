# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0004_auto_20150908_2153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Number',
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
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=16)),
                ('active', models.BooleanField()),
                ('last_sent', models.DateTimeField(blank=True)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Messages',
            new_name='Message',
        ),
        migrations.RenameModel(
            old_name='Variables',
            new_name='Variable',
        ),
        migrations.RemoveField(
            model_name='numbers',
            name='subscription_id',
        ),
        migrations.RemoveField(
            model_name='subscriptions',
            name='message_id',
        ),
        migrations.AlterModelOptions(
            name='unconfirmed',
            options={'verbose_name_plural': 'Unconfirmed'},
        ),
        migrations.AlterField(
            model_name='unconfirmed',
            name='subscription_id',
            field=models.ForeignKey(to='Factz.Subscription'),
        ),
        migrations.DeleteModel(
            name='Numbers',
        ),
        migrations.DeleteModel(
            name='Subscriptions',
        ),
        migrations.AddField(
            model_name='subscription',
            name='message_id',
            field=models.ForeignKey(to='Factz.Message'),
        ),
        migrations.AddField(
            model_name='number',
            name='subscription_id',
            field=models.ForeignKey(to='Factz.Subscription'),
        ),
    ]

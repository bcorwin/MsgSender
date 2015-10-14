# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0042_auto_20151013_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentmessage',
            name='followup_status',
            field=models.IntegerField(default=None, null=True, choices=[(-1, 'Not active.'), (-2, 'No follow up.'), (0, 'Success'), (1, 'Unknown error'), (3, 'Invalid type'), (30001, 'Queue overflow'), (30002, 'Account suspended'), (30003, 'Unreachable destination handset'), (30004, 'Message blocked'), (30005, 'Unknown destination handset'), (30006, 'Landline or unreachable carrier'), (30007, 'Carrier violation'), (30008, 'Unknown error'), (30009, 'Missing segment')], blank=True),
        ),
        migrations.AddField(
            model_name='sentmessage',
            name='message_status',
            field=models.IntegerField(default=None, null=True, choices=[(-1, 'Not active.'), (-2, 'No follow up.'), (0, 'Success'), (1, 'Unknown error'), (3, 'Invalid type'), (30001, 'Queue overflow'), (30002, 'Account suspended'), (30003, 'Unreachable destination handset'), (30004, 'Message blocked'), (30005, 'Unknown destination handset'), (30006, 'Landline or unreachable carrier'), (30007, 'Carrier violation'), (30008, 'Unknown error'), (30009, 'Missing segment')], blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

ALTER TABLE Factz.sentMessage ALTER COLUMN attempted TYPE integer USING (CASE attempted when TRUE then 1 when FALSE then 0 END);

class Migration(migrations.Migration):

    dependencies = [
        ('Factz', '0041_remove_subscription_last_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessage',
            name='attempted',
            field=models.IntegerField(choices=[(0, 'Not attempted'), (1, 'Message attempted'), (2, 'Completed')], default=0),
        ),
    ]

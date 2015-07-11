# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0005_reconhecimento_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconhecimento',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 11, 4, 51, 8, 52442, tzinfo=utc)),
        ),
    ]

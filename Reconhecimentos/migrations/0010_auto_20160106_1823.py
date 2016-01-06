# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0009_auto_20150725_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconhecimento',
            name='data',
            field=models.DateField(auto_now_add=True),
        ),
    ]

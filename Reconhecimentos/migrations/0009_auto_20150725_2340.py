# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0008_auto_20150725_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconhecimento',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

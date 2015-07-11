# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.utils import timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0004_auto_20150711_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='reconhecimento',
            name='data',
            field=models.DateTimeField(default=timezone.now()),
        ),
    ]

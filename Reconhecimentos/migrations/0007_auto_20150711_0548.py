# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0006_auto_20150711_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconhecimento',
            name='data',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

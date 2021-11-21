# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0023_auto_20161130_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackSimplificado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descritivo', models.CharField(max_length=1000)),
            ],
        ),
    ]

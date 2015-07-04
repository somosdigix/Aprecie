# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reconhecimento',
            name='funcionario',
        ),
        migrations.AddField(
            model_name='reconhecimento',
            name='id_do_funcionario',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0002_auto_20150704_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconhecimento',
            name='funcionario',
            field=models.ForeignKey(to='Login.Funcionario'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=b'200')),
                ('cpf', models.CharField(unique=True, max_length=b'11')),
                ('data_de_nascimento', models.DateField()),
            ],
        ),
    ]

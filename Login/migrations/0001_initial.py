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
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('nome', models.CharField(max_length=b'200')),
                ('cpf', models.CharField(max_length=b'11', unique=True, serialize=False, primary_key=True)),
                ('data_de_nascimento', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

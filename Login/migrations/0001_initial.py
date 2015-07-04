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
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=b'200')),
                ('cpf', models.CharField(unique=True, max_length=b'11')),
                ('data_de_nascimento', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

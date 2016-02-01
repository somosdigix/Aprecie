# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('cpf', models.CharField(unique=True, max_length='11')),
                ('nome', models.CharField(max_length='200')),
                ('data_de_nascimento', models.DateField()),
                ('foto', models.TextField(null=True, default=None)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

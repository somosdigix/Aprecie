# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0003_inserindo_valores'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescricaoDoValor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
    ]

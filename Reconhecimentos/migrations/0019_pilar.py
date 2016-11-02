# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0018_remover_reconhecimentos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pilar',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.CharField(max_length=1000)),
            ],
        ),
    ]

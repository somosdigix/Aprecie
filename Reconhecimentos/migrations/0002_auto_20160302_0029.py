# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='valor',
            name='descricao',
            field=models.CharField(max_length=500,default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='valor',
            name='resumo',
            field=models.CharField(max_length=200,default=''),
            preserve_default=False,
        ),
    ]

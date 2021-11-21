# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0004_descricaodovalor'),
    ]

    operations = [
        migrations.AddField(
            model_name='valor',
            name='descricoes',
            field=models.ManyToManyField(to='Reconhecimentos.DescricaoDoValor'),
        ),
    ]

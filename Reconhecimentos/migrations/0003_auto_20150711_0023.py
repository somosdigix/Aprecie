# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
        ('Reconhecimentos', '0002_carregamento_dos_valores_da_digitho'),
    ]

    operations = [
        migrations.AddField(
            model_name='reconhecimento',
            name='reconhecedor',
            field=models.ForeignKey(related_name='reconhecedor', default=None, to='Login.Funcionario'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reconhecimento',
            name='funcionario',
            field=models.ForeignKey(related_name='reconhecido', to='Login.Funcionario'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0007_remove_valor_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconhecimento',
            name='justificativa',
            field=models.CharField(max_length=1000),
        ),
    ]

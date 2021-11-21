# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0020_remove_reconhecimento_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='reconhecimento',
            name='pilar',
            field=models.ForeignKey(to='Reconhecimentos.Pilar', on_delete=models.CASCADE),
        ),
    ]

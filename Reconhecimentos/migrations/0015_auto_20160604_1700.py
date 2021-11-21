# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0014_remove_reconhecimento_justificativa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconhecimento',
            name='feedback',
            field=models.ForeignKey(to='Reconhecimentos.Feedback', related_name='feedback', default=None, on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]

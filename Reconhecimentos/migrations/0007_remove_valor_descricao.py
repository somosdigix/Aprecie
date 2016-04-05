# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0006_migrar_descricoes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='valor',
            name='descricao',
        ),
    ]

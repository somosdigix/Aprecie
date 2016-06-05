# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0013_migrar_justificativas_para_novo_template_de_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reconhecimento',
            name='justificativa',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0003_colaborador_usuario_no_slack'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='teste',
            field=models.TextField(default=None, null=True),
        ),
    ]

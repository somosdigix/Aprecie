# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0004_colaborador_teste'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colaborador',
            name='teste',
        ),
    ]

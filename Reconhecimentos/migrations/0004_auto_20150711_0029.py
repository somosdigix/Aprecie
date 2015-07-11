# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0003_auto_20150711_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reconhecimento',
            old_name='funcionario',
            new_name='reconhecido',
        ),
    ]

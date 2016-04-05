# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_auto_20160302_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='usuario_no_slack',
            field=models.CharField(null=True, max_length=100),
        ),
    ]

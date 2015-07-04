# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0002_auto_20150704_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconhecimento',
            name='id_do_funcionario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

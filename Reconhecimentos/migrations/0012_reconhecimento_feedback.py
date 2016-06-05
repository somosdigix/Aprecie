# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0011_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='reconhecimento',
            name='feedback',
            field=models.ForeignKey(related_name='feedback', to='Reconhecimentos.Feedback', null=True),
        ),
    ]

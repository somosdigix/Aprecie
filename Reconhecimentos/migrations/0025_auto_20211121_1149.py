# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0024_feedbacksimplificado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reconhecimentohistorico',
            name='feedback',
        ),
        migrations.RemoveField(
            model_name='reconhecimentohistorico',
            name='reconhecedor',
        ),
        migrations.RemoveField(
            model_name='reconhecimentohistorico',
            name='reconhecido',
        ),
        migrations.RemoveField(
            model_name='reconhecimentohistorico',
            name='valor',
        ),
        migrations.AlterField(
            model_name='reconhecimento',
            name='feedback',
            field=models.ForeignKey(related_name='feedback', to='Reconhecimentos.FeedbackSimplificado'),
        ),
        migrations.DeleteModel(
            name='ReconhecimentoHistorico',
        ),
    ]

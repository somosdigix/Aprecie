# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Reconhecimentos', '0015_auto_20160604_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReconhecimentoHistorico',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('data', models.DateField()),
                ('feedback', models.ForeignKey(related_name='feedback_historico', to='Reconhecimentos.Feedback', on_delete=models.CASCADE)),
                ('reconhecedor', models.ForeignKey(related_name='reconhecedor_historico', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('reconhecido', models.ForeignKey(related_name='reconhecido_historico', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('valor', models.ForeignKey(to='Reconhecimentos.Valor', on_delete=models.CASCADE)),
            ],
        ),
    ]

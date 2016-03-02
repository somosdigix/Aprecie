# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from Reconhecimentos.models import Valor

def preencher_valores(apps, schema_editor):
    Valor.objects.create(nome='Relacionamento', resumo='Construir relações respeitando as diferenças', descricao='1')
    Valor.objects.create(nome='Segurança', resumo='Criar ambiente livre e responsável', descricao='1')
    Valor.objects.create(nome='Responsabilidade', resumo='Agir como dono', descricao='1')
    Valor.objects.create(nome='Resultado', resumo='Fazer acontecer', descricao='1')
    Valor.objects.create(nome='Inquietude', resumo='Agir sem acomodação', descricao='1')
    Valor.objects.create(nome='Alegria', resumo='Viver com empenho e leveza', descricao='1')
    Valor.objects.create(nome='Colaboração', resumo='Apoiar para fortalecer resultados', descricao='1')

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0002_auto_20160302_0029'),
    ]

    operations = [
        migrations.RunPython(preencher_valores),
    ]

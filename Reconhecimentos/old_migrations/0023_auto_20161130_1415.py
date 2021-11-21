# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def preencher_pilares(apps, schema_editor):
  Pilar = apps.get_model('Reconhecimentos', 'Pilar')
  pilar_com_nome_incorreto = Pilar.objects.get(nome = 'Planejar, entregar e aprender')
  pilar_com_nome_incorreto.nome = 'Planejar, entregar, aprender'
  pilar_com_nome_incorreto.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0022_inserindo_pilares'),
    ]

    operations = [
      migrations.RunPython(preencher_pilares),
    ]

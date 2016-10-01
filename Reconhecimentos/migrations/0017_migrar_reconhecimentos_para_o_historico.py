# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def migrar_reconhecimentos(apps, schema_editor):
  Reconhecimento = apps.get_model('Reconhecimentos', 'Reconhecimento')
  ReconhecimentoHistorico = apps.get_model('Reconhecimentos', 'ReconhecimentoHistorico')

  for reconhecimento in Reconhecimento.objects.all():
    reconhecimento_historico = ReconhecimentoHistorico.objects.create(reconhecedor = reconhecimento.reconhecedor,
      reconhecido = reconhecimento.reconhecido, feedback = reconhecimento.feedback, valor = reconhecimento.valor,
      data = reconhecimento.data)

    reconhecimento_historico.save()

class Migration(migrations.Migration):

  dependencies = [
    ('Reconhecimentos', '0016_reconhecimentohistorico'),
  ]

  operations = [
    migrations.RunPython(migrar_reconhecimentos)
  ]

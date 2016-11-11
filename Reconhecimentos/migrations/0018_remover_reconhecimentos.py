# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def remover_reconhecimentos(apps, schema_editor):
  Reconhecimento = apps.get_model('Reconhecimentos', 'Reconhecimento')

  Reconhecimento.objects.all().delete()


class Migration(migrations.Migration):
  dependencies = [
    ('Reconhecimentos', '0017_migrar_reconhecimentos_para_o_historico'),
  ]

  operations = [
    migrations.RunPython(remover_reconhecimentos)
  ]

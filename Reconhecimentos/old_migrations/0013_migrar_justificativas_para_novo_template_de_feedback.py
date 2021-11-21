# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def migrar_justificativas(apps, schema_editor):
  Reconhecimento = apps.get_model('Reconhecimentos', 'Reconhecimento')
  Feedback = apps.get_model('Reconhecimentos', 'Feedback')

  for reconhecimento in Reconhecimento.objects.all():
    feedback = Feedback.objects.create(situacao='', comportamento='', impacto=reconhecimento.justificativa)
    reconhecimento.feedback = feedback
    reconhecimento.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0012_reconhecimento_feedback'),
    ]

    operations = [
      migrations.RunPython(migrar_justificativas)
    ]

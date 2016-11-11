# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def preencher_pilares(apps, schema_editor):
  Pilar = apps.get_model('Reconhecimentos', 'Pilar')
  Pilar.objects.create(nome = 'Colaborar sempre', descricao = 'Utilizar a colaboração para criar relacionamentos com foco em resultados para todos')
  Pilar.objects.create(nome = 'Fazer diferente', descricao = 'Estimular um ambiente seguro onde a inquietude para assumir riscos e a responsabilidade para fazer acontecer caminham lado a lado')
  Pilar.objects.create(nome = 'Focar nas pessoas', descricao = 'Garantir um ambiente seguro para que as pessoas sejam o que são e assim possam construir relacionamentos com alegria')
  Pilar.objects.create(nome = 'Planejar, entregar e aprender', descricao = 'Agir com responsabilidade planejando nossas ações com foco no resultado de nossas entregas e com inquietude para aprender com nossos erros e acertos')

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0021_reconhecimento_pilar'),
    ]

    operations = [
        migrations.RunPython(preencher_pilares),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from Reconhecimentos.models import Valor

def preencherValores(apps, schema_editor):
	Valor.objects.create(nome='Inquietude')
	Valor.objects.create(nome='Proatividade')
	Valor.objects.create(nome='Resultado')
	Valor.objects.create(nome='Transparencia')
	Valor.objects.create(nome='Alegria')
	Valor.objects.create(nome='Excelência')
	Valor.objects.create(nome='Colaboração')

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(preencherValores)
    ]
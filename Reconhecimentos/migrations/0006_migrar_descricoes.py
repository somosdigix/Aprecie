# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def migrar_descricoes(apps, schema_editor):
    Valor = apps.get_model("Reconhecimentos", "Valor")
    DescricaoDoValor = apps.get_model("Reconhecimentos", "DescricaoDoValor")

    for valor in Valor.objects.all():
        for descricao in valor.descricao.split("|"):
            valor.descricoes.create(descricao=descricao)

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0005_valor_descricoes'),
    ]

    operations = [
        migrations.RunPython(migrar_descricoes)
    ]

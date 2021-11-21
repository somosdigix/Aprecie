# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def preencher_valores(apps, schema_editor):
    Valor = apps.get_model("Reconhecimentos", "Valor")
    Valor.objects.create(nome='Relacionamento', resumo='Construir relações respeitando as diferenças', descricao='Criamos relacionamentos de forma respeitosa, verdadeira e transparente|Incentivamos o feedback sem julgamentos|Compreendemos e respeitamos a individualidade, para estabelecer empatia e confiança|Tratamos a todos como queremos ser tratados')
    Valor.objects.create(nome='Segurança', resumo='Criar ambiente livre e responsável', descricao='Queremos que as pessoas tenham liberdade para assumir riscos e desenvolver seu potencial|Valorizamos um espaço compreensivo e respeitoso para exposição de opiniões;Estimulamos a atitude responsável em todas as situações|Atuamos na construção de ambiente saudável, que favorece a produtividade e a aprendizagem')
    Valor.objects.create(nome='Responsabilidade', resumo='Agir como dono', descricao='Atuamos comprometidos com o resultado coletivo|Nossas lideranças estimulam e apoiam para que as pessoas sejam melhores do que elas|Reconhecemos atitudes comprometidas no lugar de desculpas|Queremos ser e fazer melhor sempre')
    Valor.objects.create(nome='Resultado', resumo='Fazer acontecer', descricao='Resultado é tudo que gera valor para as pessoas|Concentramos esforços para transformar a realidade|Estimulamos a saída da zona de conforto para conquistar resultados incríveis')
    Valor.objects.create(nome='Inquietude', resumo='Agir sem acomodação', descricao='Promovemos a melhoria contínua nas pessoas e nas nossas soluções|Questionamos sempre para entender antes de executar|Praticamos a criatividade e inovação em tudo que realizamos')
    Valor.objects.create(nome='Alegria', resumo='Viver com empenho e leveza', descricao='Buscamos proporcionar bem estar e sensação de plenitude às pessoas|Associamos trabalho com atividades comprometidas e estimulantes|Esforçamos para contagiar a todos com nosso entusiasmo e jeito de ser')
    Valor.objects.create(nome='Colaboração', resumo='Apoiar para fortalecer resultados', descricao='Acreditamos na construção coletiva como a melhor forma de desenvolver soluções eficientes|Privilegiamos o trabalho em equipe sem heróis|Praticamos a interação próxima em todos os relacionamentos|Cultivamos o feedback como impulsionador de melhorias')

class Migration(migrations.Migration):

    dependencies = [
        ('Reconhecimentos', '0002_auto_20160302_0029'),
    ]

    operations = [
        migrations.RunPython(preencher_valores),
    ]

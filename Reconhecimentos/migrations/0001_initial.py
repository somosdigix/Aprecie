# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reconhecimento',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('justificativa', models.CharField(max_length=200)),
                ('data', models.DateField(auto_now_add=True)),
                ('reconhecedor', models.ForeignKey(related_name='reconhecedor', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('reconhecido', models.ForeignKey(related_name='reconhecido', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Valor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='reconhecimento',
            name='valor',
            field=models.ForeignKey(to='Reconhecimentos.Valor', on_delete=models.CASCADE),
        ),
    ]

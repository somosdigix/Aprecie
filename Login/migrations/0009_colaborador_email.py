# Generated by Django 4.1.2 on 2023-03-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0008_alter_log_administrador_descricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

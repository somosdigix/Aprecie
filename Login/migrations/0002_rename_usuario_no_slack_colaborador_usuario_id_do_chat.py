# Generated by Django 3.2.9 on 2021-11-23 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colaborador',
            old_name='usuario_no_slack',
            new_name='usuario_id_do_chat',
        ),
    ]

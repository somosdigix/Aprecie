from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length='200')),
                ('cpf', models.CharField(unique=True, max_length='11')),
                ('data_de_nascimento', models.DateField()),
            ],
        ),
    ]

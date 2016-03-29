from Login.models import Colaborador
import csv
import traceback

cpfs_existentes = list(map(lambda colaborador: colaborador.cpf, Colaborador.objects.all()))

with open('colaboradores.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    try:
        for row in spamreader:
            nome = row[1]
            cpf = row[2].replace('-', '')
            data_de_nascimento = row[6]
            
            if not cpf in cpfs_existentes:
                print('Inserindo', nome)
                Colaborador.objects.create(nome=nome, cpf=cpf, data_de_nascimento=data_de_nascimento)
    except Exception:
        traceback.print_exc()
        print('Importacao nao realizada')

print('Importacao finalizada')
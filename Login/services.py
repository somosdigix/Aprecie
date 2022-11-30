from Login.models import CPF, Colaborador
from django.db.models.functions import Lower

class ServicoDeInclusaoDeColaboradores:
	def incluir(self, colaboradores):
		contagem_de_inclusoes = 0
		cpfs_invalidos = []

		for colaborador in colaboradores:
			cpf = CPF(colaborador['cpf'])

			if not cpf.eh_valido:
				cpfs_invalidos.append(cpf.valor)
				continue

			if not Colaborador.objects.filter(cpf=cpf).exists():
				Colaborador.objects.create(nome=colaborador['nome'], cpf=cpf, \
					data_de_nascimento=colaborador['data_de_nascimento'], \
					usuario_id_do_chat=colaborador['usuario_id_do_chat']).save()
				contagem_de_inclusoes += 1

		return {
			'contagem_de_inclusoes': contagem_de_inclusoes,
			'cpfs_invalidos': cpfs_invalidos
		}

class ServicoDeBuscaDeColaboradores:
	def buscar(self,tipo_ordenacao):
		if tipo_ordenacao == 'crescente':
			colaboradores = Colaborador.objects.all().order_by(Lower("nome").asc())
		else: 
			colaboradores = Colaborador.objects.all().order_by(Lower("nome").desc())

		transformacao = lambda colaborador: { 'id': colaborador.id, 'nome': colaborador.nome_abreviado, 'data_de_nascimento': colaborador.data_de_nascimento, 'usuario_id_do_chat': colaborador.usuario_id_do_chat, 'foto': colaborador.foto }
		colaboradores = map(transformacao, colaboradores)

		return {
			'colaboradores': list(colaboradores)
		}


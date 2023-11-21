from Login.models import CPF, Colaborador
from django.core.paginator import Paginator
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
		colaboradores_mapeados = []

		if tipo_ordenacao == 'crescente':
			colaboradores = Colaborador.objects.all().order_by(Lower("nome").asc())
		else: 
			colaboradores = Colaborador.objects.all().order_by(Lower("nome").desc())

		numero_pessoas_por_pagina = 10
		paginacao = Paginator(colaboradores, numero_pessoas_por_pagina)
		numero_paginas = paginacao.num_pages
		
		for i in range(1,numero_paginas+1):
			pagina = paginacao.page(i)
			transformacao = lambda colaborador: { 'id': colaborador.id, 'nome': colaborador.nome_abreviado,'cpf': self.converter_cpf(colaborador.cpf), 'data_de_nascimento': self.converter_data(colaborador.data_de_nascimento), 'usuario_id_do_chat': colaborador.usuario_id_do_chat, 'foto': colaborador.foto }
			colaboradores_mapeados.append(list(map(transformacao, pagina.object_list)))

		return {
			'colaboradores': colaboradores_mapeados,
			'numero_paginas': numero_paginas
		}

	def converter_data(self, data):
		return data.strftime('%d/%m/%Y')

	def converter_cpf(self, cpf):
		return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

class ServicoDeBuscaDeColaborador:
	def buscar(self,id_colaborador):
		colaborador = Colaborador.objects.get(id=id_colaborador)
		return{
			'nome': colaborador.nome,
			'data_de_nascimento': colaborador.data_de_nascimento,
			'cpf': colaborador.cpf,
			'usuario_id_do_chat': colaborador.usuario_id_do_chat,
			'esta_ativo': colaborador.esta_ativo
		}

class ServicoDeEdicaoDeColaborador:
	def editar(self, colaborador, id_colaborador):
		colaborador_obtido = Colaborador.objects.get(id = id_colaborador)
		colaborador_obtido.nome = colaborador['nome']
		colaborador_obtido.cpf = colaborador['cpf']
		colaborador_obtido.usuario_id_do_chat = colaborador['usuario_id_do_chat']
		colaborador_obtido.data_de_nascimento = colaborador['data_de_nascimento']
		colaborador_obtido.esta_ativo = colaborador['esta_ativo']
		colaborador_obtido.save()
		return {
		}

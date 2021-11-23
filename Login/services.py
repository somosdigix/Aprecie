from Login.models import CPF, Colaborador

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
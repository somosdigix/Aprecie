from Login.models import Funcionario
from Aprecie.base import ExcecaoDeDominio

class ServicoDeAutenticacao:

	def autenticar(self, cpf, data_de_nascimento):
		funcionario = Funcionario.objects.filter(cpf=cpf, data_de_nascimento=data_de_nascimento)

		if not funcionario:
			raise ExcecaoDeDominio('Colaborador não encontrado, confirme seus dados e tente novamente')

		return funcionario[0]

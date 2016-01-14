from Login.models import Funcionario
from Aprecie.base import ExcecaoDeDominio

class ServicoDeAutenticacao:

	def autenticar(self, cpf, data_de_nascimento):
		funcionario = Funcionario.objects.filter(cpf=cpf, data_de_nascimento=data_de_nascimento)

		if not funcionario:
			raise ExcecaoDeDominio('Oi! Seus dados não foram encontrados. Confira tente novamente. :)')

		return funcionario[0]
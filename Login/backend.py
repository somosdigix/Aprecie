from models import Funcionario

class FuncionarioBackend(object):
	
	def authenticate(self, cpf=None, data_de_nascimento=None):
		try:
			funcionario = Funcionario.objects.get(cpf=cpf, data_de_nascimento=data_de_nascimento)
			return funcionario
		except Funcionario.DoesNotExist:
			return None

	def get_user(self, id):
		try:
			return Funcionario.objects.get(pk=id)
		except Funcionario.DoesNotExist:
			return None
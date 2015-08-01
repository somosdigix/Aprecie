import factory
from Login.models import Funcionario
from datetime import datetime, timedelta
import random

def gerar_data_aleatoria():
	anos_atras = random.randint(20, 80) * 365
	return datetime.today() - timedelta(days=anos_atras)

class FuncionarioFactory(factory.django.DjangoModelFactory):

	class Meta:
		model = Funcionario

	cpf = factory.Sequence(lambda i: str(random.randint(10000000000, 99999999999)))
	nome = "Alberto Roberto"
	data_de_nascimento = factory.Sequence(lambda i: gerar_data_aleatoria())
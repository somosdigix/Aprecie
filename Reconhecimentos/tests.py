from django.test import TestCase
from Login.models import Funcionario
from Reconhecimentos.models import Valor
from Reconhecimentos.models import Reconhecimento
from Reconhecimentos.statics import ValoresDaDigithoBrasil

class TesteDeReconhecimento(TestCase):

	def testa_o_reconhecimento_de_uma_habilidade(self):
		funcionario = Funcionario.objects.create(nome='Renan', cpf='00000000000', data_de_nascimento='2000-12-01')
		proatividade = ValoresDaDigithoBrasil.proatividade
		inquietude = ValoresDaDigithoBrasil.inquietude

		funcionario.reconhecer(proatividade, 'Foi legal');
		funcionario.reconhecer(inquietude, 'Voce realmente questiona as coisas');
		funcionario.reconhecer(proatividade, 'Parabens pela iniciativa');

		self.assertEqual(2, funcionario.reconhecimentos(proatividade))
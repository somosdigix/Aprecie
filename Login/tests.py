from django.test import TestCase
from datetime import datetime
from Login.factories import FuncionarioFactory
from Login.services import ServicoDeAutenticacao
from django.core.urlresolvers import reverse
from Login.validadores import calcular_primeiro_digito_verificador
from Login.validadores import calcular_segundo_digito_verificador
from Login.validadores import validar_cpf
import json

class TesteDoServicoDeAutenticacao(TestCase):

	def testa_a_autenticacao_de_funcionario_existente(self):
		funcionario = FuncionarioFactory()
		servicoDeAutenticacao = ServicoDeAutenticacao()

		funcionario_autenticado = servicoDeAutenticacao.autenticar(funcionario.cpf, funcionario.data_de_nascimento)

		self.assertEqual(funcionario.id, funcionario_autenticado.id)

	def testa_a_autenticacao_de_funcionario_inexistente(self):
		cpf_invalido = '09876543212'
		data_de_nascimento_invalida = datetime(2015, 8, 1)
		servicoDeAutenticacao = ServicoDeAutenticacao()

		with self.assertRaises(Exception) as contexto:
			servicoDeAutenticacao.autenticar(cpf_invalido, data_de_nascimento_invalida)
		
		self.assertEqual('Colaborador não encontrado, confirme seus dados e tente novamente', contexto.exception.args[0])

class TesteDeAutenticacao(TestCase):

	def testa_autenticacao_de_funcionario_existente(self):
		funcionario = FuncionarioFactory()
		dados_da_requisicao = dict(cpf=funcionario.cpf, data_de_nascimento=funcionario.data_de_nascimento.strftime('%d/%m/%Y'))

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(funcionario.id, resposta_json['id_do_colaborador'])
		self.assertEqual(funcionario.nome, resposta_json['nome_do_colaborador'])

	def testa_autenticacao_de_funcionario_inexistente(self):
		cpf = 'um cpf qualquer'
		data_de_nascimento = '02/01/2001'
		dados_da_requisicao = dict(cpf=cpf, data_de_nascimento=data_de_nascimento)

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)
		
		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual('Colaborador não encontrado, confirme seus dados e tente novamente', resposta_json['mensagem'])


class TesteDeValidadorDeCPF(TestCase):
	
	def testa_o_calculo_do_primeiro_digito(self):
		numeros = [1, 1, 1, 4, 4, 4, 7, 7, 7]

		primeiro_digito_verificador = calcular_primeiro_digito_verificador(numeros)

		self.assertEqual(3, primeiro_digito_verificador)

	def testa_o_calculo_do_segundo_digito(self):
		numeros = [1, 1, 1, 4, 4, 4, 7, 7, 7, 3]

		segundo_digito_verificador = calcular_segundo_digito_verificador(numeros)

		self.assertEqual(5, segundo_digito_verificador)

	def testa_a_validacao_de_um_cpf(self):
		cpf = "11144477735"
		self.assertTrue(validar_cpf(cpf))


from django.core.exceptions import ValidationError

class TesteDeFuncionario(TestCase):

	def testa_que_nao_criar_pessoa_com_cpf_invalido(self):
		from Login.models import Funcionario
		with self.assertRaises(ValidationError) as contexto:
			FuncionarioFactory(cpf="11144477700", nome="dsadsa", data_de_nascimento=datetime.today())
		self.assertEqual("CPF inválido", contexto.exception.args[0])
from django.test import TestCase
from datetime import datetime
from Login.factories import FuncionarioFactory
from Login.services import ServicoDeAutenticacao
from django.core.urlresolvers import reverse
import json
from Aprecie.base import ExcecaoDeDominio

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
		self.assertEqual(funcionario.nome_compacto, resposta_json['nome_do_colaborador'])

	def testa_autenticacao_de_funcionario_inexistente(self):
		cpf = 'um cpf qualquer'
		data_de_nascimento = '02/01/3001'
		dados_da_requisicao = dict(cpf=cpf, data_de_nascimento=data_de_nascimento)

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)
		
		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(403, resposta.status_code)
		self.assertEqual('Colaborador não encontrado, confirme seus dados e tente novamente', resposta_json['mensagem'])

	def testa_que_a_foto_do_colaborador_eh_alterada(self):
		nova_foto = 'base64=???'
		colaborador = FuncionarioFactory()
		dados_da_requisicao = {
			'nova_foto': nova_foto,
			'id_do_colaborador': colaborador.id
		}

		resposta = self.client.post(reverse('alterar_foto'), dados_da_requisicao)

		colaborador.refresh_from_db()
		self.assertEqual(nova_foto, colaborador.foto)

class TesteDeColaborador(TestCase):

	def testa_que_a_foto_deve_ser_alterada(self):
		nova_foto = 'base64=????'
		colaborador = FuncionarioFactory()

		colaborador.alterar_foto(nova_foto)

		self.assertEqual(nova_foto, colaborador.foto)

	def testa_que_nao_deve_trocar_para_uma_foto_inexistente(self):
		colaborador = FuncionarioFactory()

		with self.assertRaises(ExcecaoDeDominio) as contexto:
			colaborador.alterar_foto(' ')

		self.assertEqual('Foto deve ser informada', contexto.exception.args[0])
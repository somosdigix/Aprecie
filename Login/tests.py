from django.test import TestCase
from datetime import datetime
from Login.factories import ColaboradorFactory
from django.core.urlresolvers import reverse
from Aprecie.base import ExcecaoDeDominio
import json

class TesteDeColaborador(TestCase):
	def setUp(self):
		colaborador = ColaboradorFactory()
		dados_da_requisicao = dict(cpf=colaborador.cpf, data_de_nascimento=colaborador.data_de_nascimento.strftime('%d/%m/%Y'))
		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

	def testa_que_a_foto_do_colaborador_eh_alterada(self):
		nova_foto = 'base64=???'
		colaborador = ColaboradorFactory()
		dados_da_requisicao = {
			'nova_foto': nova_foto,
			'id_do_colaborador': colaborador.id
		}

		resposta = self.client.post(reverse('alterar_foto'), dados_da_requisicao)

		colaborador.refresh_from_db()
		self.assertEqual(nova_foto, colaborador.foto)

	def testa_que_deve_retornar_a_lista_de_colaboradores_ja_com_nome_abreviado(self):
		ColaboradorFactory()

		resposta = self.client.get(reverse('obter_colaboradores'))

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual('Alberto Roberto', resposta_json['colaboradores'][0]['nome'])

	def testa_que_a_foto_deve_ser_alterada(self):
		nova_foto = 'base64=????'
		colaborador = ColaboradorFactory()

		colaborador.alterar_foto(nova_foto)

		self.assertEqual(nova_foto, colaborador.foto)

	def testa_que_nao_deve_trocar_para_uma_foto_inexistente(self):
		colaborador = ColaboradorFactory()

		with self.assertRaises(ExcecaoDeDominio) as contexto:
			colaborador.alterar_foto(' ')

		self.assertEqual('Foto deve ser informada', contexto.exception.args[0])

	def testa_que_deve_exibir_somente_o_primeiro_nome(self):
		colaborador = ColaboradorFactory()

		self.assertEqual('Alberto', colaborador.primeiro_nome)

	def testa_que_deve_abreviar_o_nome_da_pessoa(self):
		colaborador = ColaboradorFactory()

		self.assertEqual('Alberto Roberto', colaborador.nome_abreviado)


class TesteDeAutenticacao(TestCase):

	def testa_autenticacao_de_colaborador_existente(self):
		colaborador = ColaboradorFactory()
		dados_da_requisicao = dict(cpf=colaborador.cpf, data_de_nascimento=colaborador.data_de_nascimento.strftime('%d/%m/%Y'))

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(colaborador.id, resposta_json['id_do_colaborador'])
		self.assertEqual(colaborador.primeiro_nome, resposta_json['nome_do_colaborador'])

	def testa_autenticacao_de_colaborador_inexistente(self):
		cpf = 'um cpf qualquer'
		data_de_nascimento = '02/01/3001'
		dados_da_requisicao = dict(cpf=cpf, data_de_nascimento=data_de_nascimento)

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)
		
		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(403, resposta.status_code)
		self.assertEqual('Oi! Seus dados não foram encontrados. Confira tente novamente. :)', resposta_json['mensagem'])

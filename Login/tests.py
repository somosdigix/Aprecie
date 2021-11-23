import json
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.db.utils import IntegrityError

from Aprecie.base import ExcecaoDeDominio
from Aprecie.settings import ADMIN_TOKEN
from Login.factories import ColaboradorFactory
from Login.models import CPF, Colaborador
from Login.services import ServicoDeInclusaoDeColaboradores
from Reconhecimentos.models import Pilar
from Reconhecimentos.factories import FeedbackFactory

class TesteDeCpf(TestCase):
	def testa_que_deve_validar_um_cpf_valido(self):
		cpf_valido = '29787427398'
		
		cpf = CPF(cpf_valido)

		self.assertTrue(cpf.eh_valido)

	def testa_que_deve_validar_um_cpf_invalido(self):
		cpf_invalido = '12312312321'
		
		cpf = CPF(cpf_invalido)

		self.assertFalse(cpf.eh_valido)

	def testa_que_deve_limpar_o_valor_caso_hajam_mascaras(self):
		cpf_com_mascara = '421.289.469-64'
		cpf_com_mascara_e_sujeiras = ' 617.529 .995-76   '
		
		self.assertEqual(CPF(cpf_com_mascara).valor, '42128946964')
		self.assertEqual(CPF(cpf_com_mascara_e_sujeiras).valor, '61752999576')

	def testa_que_deve_se_representar_como_texto(self):
		valor = '29787427398'
		
		cpf = CPF(valor)

		self.assertEqual(valor, str(cpf))

	def testa_que_deve_se_representar_como_texto_sem_sujeiras(self):
		valor = '297.874.273-98'
		
		cpf = CPF(valor)

		self.assertEqual('29787427398', str(cpf))

class TesteDeColaboradores(TestCase):
	def setUp(self):
		self.colaborador = ColaboradorFactory()
		self.reconhecedor = ColaboradorFactory()
		
		self.pilar = Pilar.objects.create(nome='Colaborar sempre', descricao='Descrição do pilar de colaborar sempre')
		self.pilar.save()
		
		self.outroPilar = Pilar.objects.create(nome='Fazer diferente', descricao='Descrição do pilar de fazer diferente')
		self.outroPilar.save()

		self.feedback = FeedbackFactory()

	def testa_que_nao_devem_existir_colaboradores_com_cpfs_iguais(self):
		colaborador = Colaborador.objects.create(nome='nome', \
			cpf='cpf', data_de_nascimento='1989-12-31')
		colaborador.save()

		with self.assertRaises(IntegrityError) as contexto:
			Colaborador.objects.create(nome=colaborador.nome, \
				cpf=colaborador.cpf, data_de_nascimento=colaborador.data_de_nascimento)

		self.assertEqual('UNIQUE constraint failed: Login_colaborador.cpf', contexto.exception.args[0])

	def testa_que_a_foto_do_colaborador_eh_alterada(self):
		nova_foto = 'base64=???'
		dados_da_requisicao = {
			'nova_foto': nova_foto,
			'id_do_colaborador': self.colaborador.id
		}

		self.client.post(reverse('alterar_foto'), dados_da_requisicao)

		self.colaborador.refresh_from_db()
		self.assertEqual(nova_foto, self.colaborador.foto)

	def testa_que_deve_retornar_a_lista_de_colaboradores_ja_com_nome_abreviado(self):
		resposta = self.client.get(reverse('obter_colaboradores'))

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual('Alberto Roberto', resposta_json['colaboradores'][0]['nome'])

	def testa_que_a_foto_deve_ser_alterada(self):
		nova_foto = 'base64=????'

		self.colaborador.alterar_foto(nova_foto)

		self.assertEqual(nova_foto, self.colaborador.foto)

	def testa_que_nao_deve_trocar_para_uma_foto_inexistente(self):
		with self.assertRaises(ExcecaoDeDominio) as contexto:
			self.colaborador.alterar_foto(' ')

		self.assertEqual('Foto deve ser informada', contexto.exception.args[0])

	def testa_que_deve_exibir_somente_o_primeiro_nome(self):
		self.assertEqual('Alberto', self.colaborador.primeiro_nome)

	def testa_que_deve_abreviar_o_nome_da_pessoa(self):
		self.assertEqual('Alberto Roberto', self.colaborador.nome_abreviado)

	def testa_que_o_colaborador_nao_pode_reconhecer_sem_informar_seu_feedback(self):
		with self.assertRaises(Exception) as contexto:
			self.colaborador.reconhecer(self.reconhecedor, self.pilar, None)

		self.assertEqual('Feedback deve ser informado', contexto.exception.args[0])

	def testa_o_reconhecimento_de_uma_habilidade(self):
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)
		reconhecimento = self.colaborador.reconhecimentos()[0]

		self.assertEqual(1, len(self.colaborador.reconhecimentos_por_pilar(self.pilar)))
		self.assertEqual(self.reconhecedor, reconhecimento.reconhecedor)
		self.assertEqual(self.pilar, reconhecimento.pilar)

	def testa_que_feedback_esta_no_formato_simplificado(self):
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)
		reconhecimento = self.colaborador.reconhecimentos()[0]

		self.assertEqual(self.feedback.descritivo, reconhecimento.feedback.descritivo)

	def testa_que_armazena_a_data_do_reconhecimento(self):
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)
		reconhecimento = self.colaborador.reconhecimentos()[0]

		agora = timezone.now()
		self.assertEqual(agora.year, reconhecimento.data.year)
		self.assertEqual(agora.month, reconhecimento.data.month)
		self.assertEqual(agora.day, reconhecimento.data.day)

	def testa_a_listagem_de_reconhecimentos(self):
		segundoFeedback = FeedbackFactory(descritivo = 'Descritivo 2')

		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, segundoFeedback)

		pilares_esperados = [ self.pilar, self.pilar ]
		pilar_reconhecidos = map(lambda reconhecimento: reconhecimento.pilar, self.colaborador.reconhecimentos())
		self.assertEqual(pilares_esperados, list(pilar_reconhecidos))

	def testa_a_listagem_de_reconhecimentos_por_pilar(self):
		segundoFeedback = FeedbackFactory(descritivo = 'Descritivo 2')
		terceiroFeedback = FeedbackFactory(descritivo = 'Descritivo 3')

		self.colaborador.reconhecer(self.reconhecedor, self.outroPilar, self.feedback)
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, segundoFeedback)
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, terceiroFeedback)

		self.assertEqual(1, len(self.colaborador.reconhecimentos_por_pilar(self.outroPilar)))
		self.assertEqual(2, len(self.colaborador.reconhecimentos_por_pilar(self.pilar)))

	def testa_que_o_colaborador_nao_pode_se_reconher(self):
		with self.assertRaises(Exception) as contexto:
			self.colaborador.reconhecer(self.colaborador, self.pilar, self.feedback)

		self.assertEqual('O colaborador nao pode reconher a si próprio', contexto.exception.args[0])

	def testa_que_o_colaborador_nao_pode_receber_um_reconhecimento_duplicado(self):
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)

		with self.assertRaises(Exception) as contexto:
			self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)

		self.assertEqual('Não é possível reconhecer uma pessoa duas vezes pelos mesmos motivos', contexto.exception.args[0])

	def testa_que_deve_incluir_colaboradores(self):
		cabecalho_com_admin_token = {'HTTP_AUTHORIZATION': ADMIN_TOKEN}
		dados_da_requisicao = json.dumps({
			'colaboradores': [
				{ 'cpf': '100.016.740-21', 'nome': 'nome 1', 'data_de_nascimento': '1989-08-31', 'usuario_id_do_chat': '1' },
				{ 'cpf': '494.734.520-98', 'nome': 'nome 2', 'data_de_nascimento': '1989-09-30', 'usuario_id_do_chat': '1' },
				{ 'cpf': '494.734.520-98', 'nome': 'nome 3', 'data_de_nascimento': '1989-10-31', 'usuario_id_do_chat': '1' },
				{ 'cpf': '062.975.370-97', 'nome': 'nome 4', 'data_de_nascimento': '1989-11-30', 'usuario_id_do_chat': '1' },
				{ 'cpf': '111.122.333-44', 'nome': 'nome 5', 'data_de_nascimento': '1989-12-31', 'usuario_id_do_chat': '1' }
			]
		})

		resposta = self.client.post(reverse('colaborador'), content_type='application/json', \
			data=dados_da_requisicao, **cabecalho_com_admin_token)

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(3, resposta_json['contagem_de_inclusoes'])
		self.assertTrue('11112233344' in resposta_json['cpfs_invalidos'])

class TesteDeAutenticacao(TestCase):
	def testa_autenticacao_de_colaborador_existente(self):
		colaborador = ColaboradorFactory()
		colaborador.save()
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
		self.assertEqual('Oi! Seus dados não foram encontrados. Confira e tente novamente. :)', resposta_json['mensagem'])

class TesteDoServicoDeInclusaoDeColaboradores(TestCase):
	def setUp(self):
		self.nome = 'José Alberto'
		self.cpf = '42128946964'
		self.data_de_nascimento = '1989-12-31'
		self.servico = ServicoDeInclusaoDeColaboradores()

	def testa_que_deve_incluir_um_usuario(self):
		usuario_id_do_chat = '123123213'
		colaboradores_para_inclusao = [
			self.criar_colaborador_para_o_dicionario(self.nome, self.cpf, self.data_de_nascimento, usuario_id_do_chat)
		]
		
		self.servico.incluir(colaboradores_para_inclusao)

		colaborador_obtido = self.obter_colaboradores_por_cpf(self.cpf)[0]
		self.assertEqual(self.nome, colaborador_obtido.nome)
		self.assertEqual(self.cpf, colaborador_obtido.cpf)
		self.assertEqual(self.data_de_nascimento, colaborador_obtido.data_de_nascimento.strftime('%Y-%m-%d'))
		self.assertEqual(usuario_id_do_chat, colaborador_obtido.usuario_id_do_chat)

	def testa_que_deve_incluir_mais_de_um_usuario(self):
		outro_cpf_esperado = '61752999576'
		colaboradores_para_inclusao = [
			self.criar_colaborador_para_o_dicionario(self.nome, self.cpf, self.data_de_nascimento),
			self.criar_colaborador_para_o_dicionario(self.nome, outro_cpf_esperado, self.data_de_nascimento)
		]
		
		self.servico.incluir(colaboradores_para_inclusao)

		colaboradores = self.obter_colaboradores_por_cpf(self.cpf, outro_cpf_esperado)
		self.assertEqual(2, len(colaboradores))
		self.assertEqual(self.cpf, colaboradores[0].cpf)
		self.assertEqual(outro_cpf_esperado, colaboradores[1].cpf)

	def testa_que_deve_ignorar_usuarios_ja_existentes(self):
		outro_cpf_esperado = '61752999576'
		cpf_duplicado = self.cpf
		Colaborador.objects.create(nome=self.nome, \
				cpf=self.cpf, data_de_nascimento=self.data_de_nascimento).save()
		colaboradores_para_inclusao = [
			self.criar_colaborador_para_o_dicionario(self.nome, self.cpf, self.data_de_nascimento),
			self.criar_colaborador_para_o_dicionario(self.nome, outro_cpf_esperado, self.data_de_nascimento),
			self.criar_colaborador_para_o_dicionario(self.nome, cpf_duplicado, self.data_de_nascimento)
		]
		
		self.servico.incluir(colaboradores_para_inclusao)

		colaboradores = self.obter_colaboradores_por_cpf(self.cpf, outro_cpf_esperado, cpf_duplicado)
		self.assertEqual(2, len(colaboradores))
		self.assertEqual(self.cpf, colaboradores[0].cpf)
		self.assertEqual(outro_cpf_esperado, colaboradores[1].cpf)

	def testa_que_deve_informar_quantos_usuarios_foram_adicionados_ja_considerando_casos_duplicados(self):
		outro_cpf = '61752999576'
		cpf_duplicado = self.cpf
		colaboradores_para_inclusao = [
			self.criar_colaborador_para_o_dicionario(self.nome, self.cpf, self.data_de_nascimento),
			self.criar_colaborador_para_o_dicionario(self.nome, outro_cpf, self.data_de_nascimento),
			self.criar_colaborador_para_o_dicionario(self.nome, cpf_duplicado, self.data_de_nascimento)
		]
		
		retorno = self.servico.incluir(colaboradores_para_inclusao)

		colaboradores = self.obter_colaboradores_por_cpf(self.cpf, outro_cpf, cpf_duplicado)
		self.assertEqual(2, len(colaboradores))
		self.assertEqual(2, retorno['contagem_de_inclusoes'])

	def testa_que_deve_ignorar_os_que_possuem_cpf_invalido(self):
		cpf_invalido = '213123213'
		colaboradores_para_inclusao = [
			self.criar_colaborador_para_o_dicionario(self.nome, self.cpf, self.data_de_nascimento),
			self.criar_colaborador_para_o_dicionario(self.nome, cpf_invalido, self.data_de_nascimento),
		]
		
		self.servico.incluir(colaboradores_para_inclusao)

		colaboradores = self.obter_colaboradores_por_cpf(self.cpf, cpf_invalido)
		self.assertEqual(1, len(colaboradores))

	def testa_que_deve_informar_quais_cpf_foram_ignorados_por_estarem_invalidos(self):
		cpf_invalido = '213123213'
		colaboradores_para_inclusao = [
			self.criar_colaborador_para_o_dicionario(self.nome, self.cpf, self.data_de_nascimento),
			self.criar_colaborador_para_o_dicionario(self.nome, cpf_invalido, self.data_de_nascimento),
		]
		
		retorno = self.servico.incluir(colaboradores_para_inclusao)

		colaboradores = self.obter_colaboradores_por_cpf(self.cpf, cpf_invalido)
		self.assertEqual(1, len(colaboradores))
		self.assertTrue(cpf_invalido in retorno['cpfs_invalidos'])

	def obter_colaboradores_por_cpf(self, *cpfs):
		return Colaborador.objects.filter(cpf__in = cpfs).order_by('cpf')

	def criar_colaborador_para_o_dicionario(self, nome, cpf, data_de_nascimento, usuario_id_do_chat='1'):
		return {
			'nome': nome,
			'cpf': cpf,
			'data_de_nascimento': data_de_nascimento,
			'usuario_id_do_chat': usuario_id_do_chat
		}
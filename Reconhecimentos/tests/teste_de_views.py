import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from Login.factories import ColaboradorFactory
from Reconhecimentos.factories import ReconhecimentoFactory, ReconhecimentoHistoricoFactory, FeedbackFactory
from Reconhecimentos.models import Reconhecimento, Pilar

class TesteDeApiDeReconhecimento(TestCase):
  def logar(self, colaborador):
    dados_da_requisicao = dict(cpf=colaborador.cpf, data_de_nascimento=colaborador.data_de_nascimento.strftime('%d/%m/%Y'))
    resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

  def setUp(self):
    self.reconhecido = ColaboradorFactory()
    self.reconhecedor = ColaboradorFactory()
    self.feedback = FeedbackFactory()
    self.pilar = Pilar.objects.get(nome='Colaborar sempre')

    self.logar(self.reconhecedor)

    self.dados_do_reconhecimento = {
      'id_do_reconhecido': self.reconhecido.id,
      'id_do_reconhecedor': self.reconhecedor.id,
      'id_do_pilar': self.pilar.id,
      'situacao': self.feedback.situacao,
      'comportamento': self.feedback.comportamento,
      'impacto': self.feedback.impacto,
    }

  def testa_o_reconhecimento_de_um_colaborador_em_um_determinado_pilar(self):
    resposta = self.client.post(reverse('reconhecer'), self.dados_do_reconhecimento)
    ultimo_reconhecimento = self.mapear_reconhecimentos(Reconhecimento.objects.all())[0]

    self.assertEqual(200, resposta.status_code)
    self.assertEqual(self.dados_do_reconhecimento, ultimo_reconhecimento)

  def testa_que_nao_eh_possivel_reconhecer_duas_vezes_a_mesma_pessoa_pelos_mesmos_motivos(self):
    resposta = self.client.post(reverse('reconhecer'), self.dados_do_reconhecimento)

    self.assertEqual(200, resposta.status_code)
    self.assertEqual(1, len(Reconhecimento.objects.all()))

  def testa_a_listagem_dos_ultimos_reconhecimentos_realizados(self):
    self.criar_reconhecimentos(2)

    resposta = self.client.post(reverse('ultimos_reconhecimentos'))
    resposta_json = json.loads(resposta.content.decode())

    self.assertEqual(200, resposta.status_code)
    self.assertEqual(2, len(resposta_json))

  def testa_que_apenas_10_reconhecimentos_sao_listados(self):
    self.criar_reconhecimentos(15)

    resposta = self.client.post(reverse('ultimos_reconhecimentos'))
    resposta_json = json.loads(resposta.content.decode())

    self.assertEqual(200, resposta.status_code)
    self.assertEqual(10, len(resposta_json))

  def testa_reconhecimentos_de_uma_pessoa_agrupados_por_reconhecedor(self):
    reconhecido = ColaboradorFactory()
    reconhecedor1 = ColaboradorFactory()
    reconhecedor2 = ColaboradorFactory()
    ReconhecimentoFactory(reconhecedor=reconhecedor1, reconhecido=reconhecido)
    ReconhecimentoFactory(reconhecedor=reconhecedor2, reconhecido=reconhecido)
    ReconhecimentoFactory(reconhecedor=reconhecedor2, reconhecido=reconhecido)

    resposta = self.client.get(reverse('reconhecimentos_por_reconhecedor', args=[reconhecido.id]))
    resultado = json.loads(resposta.content.decode())
    reconhecedores = resultado.get('reconhecedores')

    self.assertEqual(2, len(reconhecedores))
    self.assertEqual(reconhecedor1.primeiro_nome, reconhecedores[0]['reconhecedor__nome'])
    self.assertEqual(self.pilar.id, reconhecedores[0]['pilar__id'])
    self.assertEqual(1, reconhecedores[0]['quantidade_de_reconhecimentos'])
    self.assertEqual(reconhecedor2.primeiro_nome, reconhecedores[1]['reconhecedor__nome'])
    self.assertEqual(self.pilar.id, reconhecedores[1]['pilar__id'])
    self.assertEqual(2, reconhecedores[1]['quantidade_de_reconhecimentos'])

  def testa_que_deve_exibir_a_descricao_do_pilar_ao_soliticar_os_reconhecimentos_de_um_determinado_pilar(self):
    reconhecido = ColaboradorFactory()

    resposta = self.client.get(reverse('reconhecimentos_por_pilar', args=[reconhecido.id, self.pilar.id]))
    resposta_json = json.loads(resposta.content.decode())

    self.assertEqual(self.pilar.id, resposta_json['id_do_pilar'])
    self.assertEqual(self.pilar.descricao, resposta_json['descricao_do_pilar'])

  def testa_que_deve_listar_apenas_os_reconhecimentos_de_um_determinado_pilar(self):
    reconhecido = ColaboradorFactory()
    reconhecedor = ColaboradorFactory()
    pilar_diferente = Pilar.objects.get(nome = 'Fazer diferente')
    ReconhecimentoFactory(reconhecedor = reconhecedor, reconhecido = reconhecido)
    ReconhecimentoFactory(reconhecedor = reconhecedor, reconhecido = reconhecido)
    ReconhecimentoFactory(reconhecedor = reconhecedor, reconhecido = reconhecido, pilar = pilar_diferente)

    resposta = self.client.get(reverse('reconhecimentos_por_pilar', args=[reconhecido.id, self.pilar.id]))
    resposta_json = json.loads(resposta.content.decode())

    self.assertEqual(self.pilar.id, resposta_json['id_do_pilar'])
    self.assertEqual(2, len(resposta_json['reconhecimentos']))

  def testa_que_deve_listar_os_detalhes_do_reconhecimento_ao_soliticar_os_reconhecimentos_de_um_determinado_pilar(self):
    reconhecido = ColaboradorFactory()
    reconhecedor = ColaboradorFactory()
    reconhecimento = ReconhecimentoFactory(reconhecedor=reconhecedor, reconhecido=reconhecido)

    resposta = self.client.get(reverse('reconhecimentos_por_pilar', args=[reconhecido.id, self.pilar.id]))
    resposta_json = json.loads(resposta.content.decode())

    self.assertEqual(str(reconhecimento.data), resposta_json['reconhecimentos'][0]['data'])
    self.assertEqual(reconhecedor.id, resposta_json['reconhecimentos'][0]['reconhecedor__id'])
    self.assertEqual(reconhecedor.nome, resposta_json['reconhecimentos'][0]['reconhecedor__nome'])
    self.assertEqual(reconhecimento.feedback.situacao, resposta_json['reconhecimentos'][0]['feedback__situacao'])
    self.assertEqual(reconhecimento.feedback.comportamento, resposta_json['reconhecimentos'][0]['feedback__comportamento'])
    self.assertEqual(reconhecimento.feedback.impacto, resposta_json['reconhecimentos'][0]['feedback__impacto'])

  def testa_que_deve_listar_todos_os_reconhecimentos_historicos_ignorando_os_atuais(self):
    reconhecido = ColaboradorFactory()
    ReconhecimentoFactory(pk = 1, reconhecido=reconhecido)
    ReconhecimentoHistoricoFactory(pk = 2, reconhecido=reconhecido)
    ReconhecimentoHistoricoFactory(pk = 3, reconhecido=reconhecido)
    ReconhecimentoHistoricoFactory(pk = 4, reconhecido=reconhecido)
    identificadores_esperados = [ 4, 3, 2 ]

    resposta = self.client.get(reverse('reconhecimentos_historicos_do_colaborador', args=[reconhecido.id]))
    resposta_json = json.loads(resposta.content.decode())
    identificadores_dos_reconhecimentos = [reconhecimento_historico['id'] for reconhecimento_historico in resposta_json]

    self.assertEqual(identificadores_esperados, identificadores_dos_reconhecimentos)

  def testa_que_deve_indicar_quais_pilares_possuem_algum_reconhecimento(self):
    reconhecido = ColaboradorFactory()
    ReconhecimentoFactory(reconhecido = reconhecido, pilar = self.pilar)

    resposta = self.client.get(reverse('reconhecimentos_do_colaborador', args = [ reconhecido.id ]))
    resposta_json = json.loads(resposta.content.decode())

    self.assertEqual(True, resposta_json['pilares'][0]['possui_reconhecimentos'])
    self.assertEqual(False, resposta_json['pilares'][1]['possui_reconhecimentos'])
    self.assertEqual(False, resposta_json['pilares'][2]['possui_reconhecimentos'])
    self.assertEqual(False, resposta_json['pilares'][3]['possui_reconhecimentos'])

  def testa_que_deve_contar_a_quantidade_de_reconhecimentos_que_existem_por_pilar(self):
    reconhecido = ColaboradorFactory()
    pilar = Pilar.objects.get(nome = 'Fazer diferente')
    ReconhecimentoFactory(reconhecido = reconhecido, pilar = self.pilar)
    ReconhecimentoFactory(reconhecido = reconhecido, pilar = self.pilar)
    ReconhecimentoFactory(reconhecido = reconhecido, pilar = pilar)

    resposta = self.client.get(reverse('reconhecimentos_do_colaborador', args = [ reconhecido.id ]))
    resposta_json = json.loads(resposta.content.decode())

    self.assertEqual(2, resposta_json['pilares'][0]['quantidade_de_reconhecimentos'])
    self.assertEqual(1, resposta_json['pilares'][1]['quantidade_de_reconhecimentos'])
    self.assertEqual(0, resposta_json['pilares'][2]['quantidade_de_reconhecimentos'])
    self.assertEqual(0, resposta_json['pilares'][3]['quantidade_de_reconhecimentos'])

  def testa_que_deve_exibir_os_dados_do_resumidos_contendo_informacoes_do_pilar(self):
    reconhecido = ColaboradorFactory()
    dados_dos_pilares = list(map(lambda pilar: {
      'id': pilar.id,
      'nome': pilar.nome,
      'descricao': pilar.descricao,
      'possui_reconhecimentos': False,
      'quantidade_de_reconhecimentos': 0
    }, Pilar.objects.all()))

    resposta = self.client.get(reverse('reconhecimentos_do_colaborador', args = [ reconhecido.id ]))
    resposta_json = json.loads(resposta.content.decode())

    self.assertEqual(dados_dos_pilares, resposta_json['pilares'])

  def mapear_reconhecimentos(self, reconhecimentos):
    return list(map(lambda reconhecimento: {
      'id_do_reconhecido': reconhecimento.reconhecido.id,
      'id_do_reconhecedor': reconhecimento.reconhecedor.id,
      'id_do_pilar': reconhecimento.pilar.id,
      'situacao': reconhecimento.feedback.situacao,
      'comportamento': reconhecimento.feedback.comportamento,
      'impacto': reconhecimento.feedback.impacto,
    }, reconhecimentos))

  def criar_reconhecimentos(self, quantidade):
    for num in range(0, quantidade):
      dados_deste_reconhecimento = {
        'id_do_reconhecido': self.reconhecido.id,
        'id_do_reconhecedor': self.reconhecedor.id,
        'id_do_pilar': self.pilar.id,
        'situacao': self.feedback.situacao + str(num),
        'comportamento': self.feedback.comportamento + str(num),
        'impacto': self.feedback.impacto + str(num),
      }

      self.client.post(reverse('reconhecer'), dados_deste_reconhecimento)

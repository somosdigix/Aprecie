from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import formats
from Login.models import Colaborador
from Reconhecimentos.models import Pilar, Valor, Reconhecimento, ReconhecimentoHistorico, Feedback
from Reconhecimentos.services import Notificacoes
from django.db.models import Count

def reconhecer(requisicao):
  id_do_reconhecedor = requisicao.POST['id_do_reconhecedor']
  id_do_reconhecido = requisicao.POST['id_do_reconhecido']
  id_do_pilar = requisicao.POST['id_do_pilar']
  situacao = requisicao.POST['situacao']
  comportamento = requisicao.POST['comportamento']
  impacto = requisicao.POST['impacto']

  reconhecido = Colaborador.objects.get(id = id_do_reconhecido)
  reconhecedor = Colaborador.objects.get(id = id_do_reconhecedor)
  pilar = Pilar.objects.get(id = id_do_pilar)
  feedback = Feedback.objects.create(situacao = situacao, comportamento = comportamento, impacto = impacto)

  reconhecido.reconhecer(reconhecedor, pilar, feedback)
  Notificacoes.notificar_no_slack(reconhecedor, reconhecido, pilar)

  return JsonResponse({})

def ultimos_reconhecimentos(requisicao):
  reconhecimentos = Reconhecimento.objects.all().order_by('-id')[:10]

  reconhecimentos_mapeados = list(map(lambda reconhecimento: {
    'id_do_reconhecedor': reconhecimento.reconhecedor.id,
    'nome_do_reconhecedor': reconhecimento.reconhecedor.nome_abreviado,
    'id_do_reconhecido': reconhecimento.reconhecido.id,
    'nome_do_reconhecido': reconhecimento.reconhecido.nome_abreviado,
    'pilar': reconhecimento.pilar.nome,
    'situacao': reconhecimento.feedback.situacao,
    'comportamento': reconhecimento.feedback.comportamento,
    'impacto': reconhecimento.feedback.impacto,
    'data': reconhecimento.data
  }, reconhecimentos))

  return JsonResponse(reconhecimentos_mapeados, safe=False)

def reconhecimentos_do_colaborador(requisicao, id_do_reconhecido):
  reconhecido = Colaborador.objects.get(id = id_do_reconhecido)
  pilares = list(map(lambda pilar: {
    'id': pilar.id,
    'nome': pilar.nome,
    'descricao': pilar.descricao,
    'possui_reconhecimentos': len(reconhecido.reconhecimentos_por_pilar(pilar)) > 0,
    'quantidade_de_reconhecimentos': len(reconhecido.reconhecimentos_por_pilar(pilar))
  }, Pilar.objects.all()))

  return JsonResponse({ 'id': reconhecido.id, 'nome': reconhecido.nome_abreviado, 'pilares': pilares }, safe = False)

def reconhecimentos_historicos_do_colaborador(requisicao, id_do_reconhecido):
  reconhecimentos_historicos = ReconhecimentoHistorico.objects \
    .filter(reconhecido=id_do_reconhecido) \
    .order_by('-id')

  resposta = list(map(lambda reconhecimento_historico: {
      'id': reconhecimento_historico.id,
      'id_do_reconhecedor': reconhecimento_historico.reconhecedor.id,
      'nome_do_reconhecedor': reconhecimento_historico.reconhecedor.nome_abreviado,
      'valor': reconhecimento_historico.valor.nome,
      'situacao': reconhecimento_historico.feedback.situacao,
      'comportamento': reconhecimento_historico.feedback.comportamento,
      'impacto': reconhecimento_historico.feedback.impacto,
      'data': reconhecimento_historico.data
    }, reconhecimentos_historicos))

  return JsonResponse(resposta, safe = False)

def reconhecimentos_por_reconhecedor(requisicao, id_do_reconhecido):
  reconhecedores = Reconhecimento.objects.filter(reconhecido = id_do_reconhecido) \
    .values('reconhecedor__nome', 'reconhecedor', 'reconhecedor__id', 'pilar__id') \
    .annotate(quantidade_de_reconhecimentos=Count('reconhecedor'))

  for reconhecedor in reconhecedores:
    reconhecedor['reconhecedor__nome'] = Colaborador.obter_primeiro_nome(reconhecedor['reconhecedor__nome'])

  return JsonResponse({ 'reconhecedores': list(reconhecedores) })

def todas_as_apreciacoes(requisicao, id_do_reconhecido):
  reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
  reconhecimentos = reconhecido.reconhecimentos() \
    .values('data', 'pilar__nome', 'feedback__situacao', 'feedback__comportamento', \
            'feedback__impacto', 'reconhecedor__nome', 'reconhecedor__id') \
    .order_by('-data', '-id')

  reconhecimentos_historicos = ReconhecimentoHistorico.objects \
    .filter(reconhecido=id_do_reconhecido) \
    .values('data', 'valor__nome', 'feedback__situacao', 'feedback__comportamento', \
            'feedback__impacto', 'reconhecedor__nome', 'reconhecedor__id') \
    .order_by('-id')
    
  resposta = {
    'reconhecimentos': list(reconhecimentos)
  }

  return JsonResponse(resposta)

def todos_os_pilares(requisicao):
  resposta = Pilar.objects.all()

  return JsonResponse(resposta)


def reconhecimentos_por_pilar(requisicao, id_do_reconhecido, id_do_pilar):
  reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
  pilar = Pilar.objects.get(id=id_do_pilar)
  reconhecimentos = reconhecido.reconhecimentos_por_pilar(id_do_pilar) \
    .values('data', 'feedback__situacao', 'feedback__comportamento', \
            'feedback__impacto', 'reconhecedor__nome', 'reconhecedor__id') \
    .order_by('-data', '-id')

  resposta = {
    'id_do_pilar': pilar.id,
    'nome_do_pilar': pilar.nome,
    'descricao_do_pilar': pilar.descricao,
    'id_do_reconhecido': reconhecido.id,
    'nome_do_reconhecido': reconhecido.nome_abreviado,
    'reconhecimentos': list(reconhecimentos)
  }

  return JsonResponse(resposta)
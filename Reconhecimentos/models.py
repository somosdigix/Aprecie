from datetime import date
from django.db import models
from Aprecie.base import ExcecaoDeDominio

class Pilar(models.Model):
  id = models.AutoField(primary_key=True)
  nome = models.CharField(max_length=200)
  descricao = models.CharField(max_length=1000)

  def __eq__(self, other):
    return self.nome == other.nome

  @property
  def frases_de_descricao(self):
    return list(self.descricoes.values_list('descricao', flat=True))

class Reconhecimento(models.Model):
  id = models.AutoField(primary_key=True)
  reconhecedor = models.ForeignKey('Login.Colaborador', related_name='reconhecedor', on_delete=models.CASCADE)
  reconhecido = models.ForeignKey('Login.Colaborador', related_name='reconhecido', on_delete=models.CASCADE)
  feedback = models.ForeignKey('Feedback', related_name='feedback', on_delete=models.CASCADE)
  pilar = models.ForeignKey(Pilar, on_delete=models.CASCADE)
  data = models.DateField(auto_now_add=True)
  

  def alterar_feedback(self, novo_feedback, reconhecedor):
    if self.reconhecedor != reconhecedor:
      raise ExcecaoDeDominio('O reconhecimento só pode ser alterado por quem o elaborou')
      
    if self.data != date.today():
      raise ExcecaoDeDominio('O reconhecimento só pode ser alterado no mesmo dia de sua realização')

    self.feedback = novo_feedback

class Feedback(models.Model):
  id = models.AutoField(primary_key=True)
  descritivo = models.CharField(max_length=1000)

  def __eq__(self, other):
    return self.descritivo == other.descritivo

class FeedbackSCI(models.Model):
  id = models.AutoField(primary_key=True)
  situacao = models.CharField(max_length=1000)
  comportamento = models.CharField(max_length=1000)
  impacto = models.CharField(max_length=1000)

  def __eq__(self, other):
    return self.situacao == other.situacao and self.comportamento == other.comportamento and self.impacto == other.impacto

class Ciclo(models.Model):
  id = models.AutoField(primary_key=True)  
  nome = models.CharField(max_length=25)
  data_inicial = models.DateField()
  data_final = models.DateField(null=True)

  def alterar_ciclo(self, data_final, nome):
    if data_final == None or data_final <= self.data_inicial:
      raise ExcecaoDeDominio('A data final do ciclo não pode ser igual ou maior que a data inicial') 
    self.data_final = data_final
    
    if nome == None or nome == "":
      raise ExcecaoDeDominio('O ciclo não pode ter um nome vazio')
    self.nome = nome
  
  def alterar_data_inicial_ciclo(self, data_inicial):
    if data_inicial == None:
      raise ExcecaoDeDominio('A data inicial não pode estar vazia')  
    self.data_inicial = data_inicial

    self.verificar_data_final_menor_que(data_inicial)
  
  def verificar_data_final_menor_que(self, data_inicial):
    if self.data_final != None and data_inicial >= self.data_final:
      self.data_final = None
    

  def calcular_porcentagem_progresso(self):
    calculo_periodo_ciclo = self.calcularPeriodoCiclo()
    calculo_progresso_em_dias = self.calcularProgessoEmDias()

    diferenca_periodo_e_progresso = calculo_periodo_ciclo - calculo_progresso_em_dias

    porcentagem_progresso = int(((diferenca_periodo_e_progresso / calculo_periodo_ciclo) * 100))
    return str(porcentagem_progresso)

  def calcularPeriodoCiclo(self):
    periodo_ciclo = self.data_final - self.data_inicial
    return periodo_ciclo.days
  
  def calcularProgessoEmDias(self):
    periodo_dias = self.data_final - date.today()
    return periodo_dias.days

  def calcularDiasParaIniciarCiclo(self):
    return self.data_inicial - date.today()
    
class LOG_Ciclo(models.Model):
  id = models.AutoField(primary_key=True)
  ciclo = models.ForeignKey('Ciclo', related_name='ciclo', on_delete=models.CASCADE)
  data_da_modificacao = models.DateField(auto_now=True)
  usuario_que_modificou = models.ForeignKey('Login.Colaborador', related_name='usuario_que_modificou', on_delete=models.CASCADE, null=True)
  descricao_da_alteracao = models.CharField(max_length=63)
  antiga_data_final = models.DateField(default=None, null=True)
  antigo_nome_ciclo = models.CharField(max_length=25, null=True)
  novo_nome_ciclo = models.CharField(max_length=25, null=True)
  nova_data_alterada = models.DateField(default=None, null=True)
  
  @classmethod
  def adicionar(cls, ciclo, usuario_que_modificou, descricao_da_alteracao, novo_nome_ciclo, nova_data_alterada):
    if ciclo.data_final != "":
      data_final = ciclo.data_final
    
    if ciclo.nome != None and ciclo.nome != "":
      ciclo_nome = ciclo.nome
    else:
      ciclo_nome = None
    
    return cls(ciclo = ciclo, usuario_que_modificou = usuario_que_modificou, descricao_da_alteracao = descricao_da_alteracao, novo_nome_ciclo = novo_nome_ciclo,
    nova_data_alterada = nova_data_alterada, antiga_data_final = data_final, antigo_nome_ciclo = ciclo_nome)

  @classmethod
  def adicionar_automatico(cls, ciclo):
    return cls(ciclo = ciclo, descricao_da_alteracao = "Criação do ciclo automatico sem data final", novo_nome_ciclo = ciclo.nome, antigo_nome_ciclo = ciclo.nome)

class Agradecimento(models.Model):
  id = models.AutoField(primary_key=True)
  data = models.DateField(auto_now_add=True)
  colaborador = models.ForeignKey('Login.Colaborador', related_name='colaborador', on_delete=models.CASCADE)
  reconhecimento = models.ForeignKey('Reconhecimentos.Reconhecimento', related_name='reconhecimento', on_delete=models.CASCADE)
  mensagem = models.CharField(max_length=1000)

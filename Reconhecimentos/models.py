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
  descritivo = models.CharField(max_length=220)

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
  data_inicial = models.DateField()
  data_final = models.DateField()

  def alterar_ciclo(self, data_final):
    self.data_final = data_final

class LOG_Ciclo(models.Model):
  id = models.AutoField(primary_key=True)
  ciclo = models.ForeignKey('Ciclo', related_name='ciclo', on_delete=models.CASCADE)
  data_da_modificacao = models.DateField(auto_now=True)
  usuario_que_modificou = models.ForeignKey('Login.Colaborador', related_name='usuario_que_modificou', on_delete=models.CASCADE)
  descricao_da_alteracao = models.CharField(max_length=50)

  
  
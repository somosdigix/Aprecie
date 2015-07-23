from django.db import models

class Funcionario(models.Model):
	nome = models.CharField(max_length='200')
	cpf = models.CharField(max_length='11', unique=True)
	data_de_nascimento = models.DateField()
	foto = models.TextField(default=None, null=True)

	@property
	def nome_compacto(self):
		nomes = self.nome.split(' ')
		return "{0} {1}".format(nomes[0], nomes[-1])

	def alterar_foto(self, nova_foto_em_base64):
		if not nova_foto_em_base64.strip():
			raise Exception('Foto deve ser informada')
			
		self.foto = nova_foto_em_base64

	def reconhecer(self, reconhecedor, valor, justificativa):
		if reconhecedor == self:
			raise Exception('O colaborador nao pode reconher a si próprio')

		if not justificativa.strip():
			raise Exception('A sua justificativa deve ser informada')

		self.reconhecido.create(reconhecedor=reconhecedor, valor=valor, justificativa=justificativa)

	def reconhecimentos(self):
		return self.reconhecido.all()

	def reconhecimentos_por_valor(self, valor):
		return self.reconhecido.filter(valor=valor)
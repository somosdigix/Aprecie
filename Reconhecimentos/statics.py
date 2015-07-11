from Reconhecimentos.models import Valor

class ValoresDaDigithoBrasil():
	inquietude = Valor.objects.get(nome='Inquietude')
	responsabilidade = Valor.objects.get(nome='Responsabilidade')
	resultado = Valor.objects.get(nome='Resultado')
	transparencia = Valor.objects.get(nome='Transparência')
	alegria = Valor.objects.get(nome='Alegria')
	excelencia = Valor.objects.get(nome='Excelência')
	colaboracao = Valor.objects.get(nome='Colaboração')
	todos = Valor.objects.all()
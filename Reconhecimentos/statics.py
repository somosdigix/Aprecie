from Reconhecimentos.models import Valor

class ValoresDaDigithoBrasil():
	proatividade = Valor.objects.get(nome='Proatividade')
	inquietude = Valor.objects.get(nome='Inquietude')
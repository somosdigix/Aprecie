class ExcecaoDeDominio(Exception):
	pass

def acesso_anonimo(funcao):
	funcao.permite_acesso_anonimo = True
	return funcao

def permite_acesso_anonimo(view):
	try:
		return view.permite_acesso_anonimo
	except AttributeError:
		return False
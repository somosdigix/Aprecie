class ExcecaoDeDominio(Exception):
	pass

def acesso_exclusivo_com_token(funcao):
	print('oi')
	funcao.acesso_exclusivo_com_token = True
	return funcao

def verificar_se_deve_acessar_somente_com_token(view):
	try:
		return view.acesso_exclusivo_com_token
	except AttributeError:
		return False

def acesso_anonimo(funcao):
	funcao.permite_acesso_anonimo = True
	return funcao

def permite_acesso_anonimo(view):
	try:
		return view.permite_acesso_anonimo
	except AttributeError:
		return False
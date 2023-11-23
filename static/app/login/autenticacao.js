define(function () {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;
		_sandbox.escutar('autenticar', validarAutenticacao);
	};

	self.finalizar = function () {
		_sandbox.removerEscuta('autenticar');
	};

	function validarAutenticacao(cpf, dataDeNascimento, estaAtivo) {
		var parametros = {
			cpf: cpf,
			data_de_nascimento: dataDeNascimento,
			esta_ativo: estaAtivo
		};

		validarOperacao(parametros);

		_sandbox.post('/login/entrar/', parametros).then(autenticar);
	}

	function autenticar(colaborador) {
		_sandbox.preencherSessao(colaborador);
		_sandbox.preencherCookie(colaborador);

		localStorage.setItem('notificacao', 'true');
		_sandbox.redirecionarPara('/app/#/perfil/' + colaborador.id_do_colaborador);
	}

	function validarOperacao(parametros) {
		if (parametros.cpf === '' || parametros.cpf === undefined)
			throw new ViolacaoDeRegra('CPF deve ser informado');

		if (parametros.data_de_nascimento === '' || parametros.data_de_nascimento === undefined)
			throw new ViolacaoDeRegra('Data de nascimento deve ser informada');
		if (parametros.esta_ativo === 0)
			throw new ViolacaoDeRegra('Usuário inativo');
	}

	return self;
});
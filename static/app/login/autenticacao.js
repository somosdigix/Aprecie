define(function() {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;
		_sandbox.escutar('autenticar', validarAutenticacao);
	};

	function validarAutenticacao(cpf, dataDeNascimento) {
		var loginViewModel = new LoginViewModel();

		validarOperacao(loginViewModel);

		_sandbox.post('/login/entrar/', loginViewModel).then(autenticar);
	}

	function autenticar(colaborador) {
		// TODO: Transformar em modulo e desacoplar esta dependência
		require(['app/servicos/servicoDeAutenticacao'], function(servicoDeAutenticacao) {
			servicoDeAutenticacao.autenticar(colaborador);
			_sandbox.navegarPara('/paginaInicial');
		});
	}

	function validarOperacao(loginViewModel) {
		if (loginViewModel.cpf === '')
			throw new ViolacaoDeRegra('CPF deve ser informado');

		if (loginViewModel.data_de_nascimento === '')
			throw new ViolacaoDeRegra('Data de nascimento deve ser informada');
	}

	function LoginViewModel() {
		var self = this;

		self.cpf = $('#cpf').val().replace(/\./g, '').replace('-', '');
		self.data_de_nascimento = $('#dataDeNascimento').val();
	}

	return self;
});
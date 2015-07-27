define([
	'jquery',
	'template',
	'text!partials/loginTemplate.html',
	'configuracoes',
	'jquery.inputmask'
], function($, template, loginTemplate, configuracoes) {
	'use strict';

	var loginView = {};

	loginView.exibir = function() {
		template.exibir(loginTemplate);
		$('body').removeClass('body-app').addClass('body-login');
		$('#conteudo').off().on('click', 'button[data-js="autenticar"]', autenticar);

		$('#cpf').inputmask('999.999.999-99').focus();
		$('#dataDeNascimento').inputmask('d/m/y');

		if (configuracoes.ehDebug()) {
			$('#cpf').val('00000000000');
			$('#dataDeNascimento').val('01/01/2015');
		}
	};

	function autenticar(evento) {
		evento.preventDefault();

		require([
			'app/models/loginViewModel',
			'app/servicos/servicoDeAutenticacao',
			'roteador'
		], function(LoginViewModel, servicoDeAutenticacao, roteador) {
			var loginViewModel = new LoginViewModel();
			validarOperacao(loginViewModel);

			$.post('/login/entrar/', loginViewModel, function(colaborador) {
				servicoDeAutenticacao.autenticar(colaborador);
				roteador.navegarPara('/paginaInicial');
			});
		});
	}

	function validarOperacao(loginViewModel) {
		if (loginViewModel.cpf === '')
			throw new ViolacaoDeRegra('CPF deve ser informado');

		if (loginViewModel.data_de_nascimento === '')
			throw new ViolacaoDeRegra('Data de nascimento deve ser informada');
	}

	return loginView;
});
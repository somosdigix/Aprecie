define([
	'jquery',
	'handlebars',
	'text!partials/loginTemplate.html',
	'configuracoes',
	'jquery.inputmask'
], function($, Handlebars, loginTemplate, configuracoes) {
	'use strict';

	var loginView = {};

	loginView.exibir = function() {
		$('#conteudo').empty().html(loginTemplate);
		$('#conteudo').off().on('click', '[data-js="autenticar"]', autenticar);

		$('#cpf').inputmask('999.999.999-99').focus();
		$('#dataDeNascimento').inputmask('d/m/y', {
			'placeholder': 'dd/mm/aaaa'
		});

		if (configuracoes.ehDebug()) {
			$('#cpf').val('00000000000');
			$('#dataDeNascimento').val('01/01/2015');
		}
	};

	function autenticar(evento) {
		evento.preventDefault();

		require([
			'app/models/loginViewModel',
			'app/models/sessaoDeUsuario',
			'app/views/buscarColaboradorView',
			'app/views/paginaInicialView'
		], function(LoginViewModel, sessaoDeUsuario, buscarColaboradorView, paginaInicialView) {
			var loginViewModel = new LoginViewModel();
			validarOperacao(loginViewModel);

			$.post('/login/entrar/', loginViewModel, function(resposta) {
				sessaoDeUsuario.preencherDados(resposta);
				buscarColaboradorView.exibir(paginaInicialView.exibir);
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
define([
	'jquery',
	'handlebars',
	'text!partials/loginTemplate.html'
], function($, Handlebars, loginTemplate) {
	'use strict';

	var loginView = {};

	loginView.exibir = function() {
		$('#conteudo').empty().html(loginTemplate);
		$('#conteudo').off().on('click', '[data-js="autenticar"]', autenticar);
	};

	function autenticar(evento) {
		evento.preventDefault();

		var loginViewModel = new LoginViewModel();

		$.post('/login/entrar/', loginViewModel, function(resposta) {
			$('[data-js="mensagem-de-validacao"]').hide();

			if (resposta.autenticado === false) {
				$('[data-js="mensagem-de-validacao"]').show().text(resposta.mensagem);
				return;
			}

			require([
				'app/models/sessaoDeUsuario',
				'app/views/buscarColaboradorView'
			], function(sessaoDeUsuario, buscarColaboradorView) {
				sessaoDeUsuario.definirId(resposta.id_do_colaborador);
				buscarColaboradorView.exibir();
			});
		});
	}

	function LoginViewModel() {
		var self = this;

		self.cpf = $('#cpf').val();
		self.data_de_nascimento = $('#dataDeNascimento').val();
	}

	return loginView;
});
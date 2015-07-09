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

		$('#cpf').inputmask('999.999.999-99');
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
			'app/views/buscarColaboradorView'
		], function(LoginViewModel, sessaoDeUsuario, buscarColaboradorView) {
			var loginViewModel = new LoginViewModel();

			$.post('/login/entrar/', loginViewModel, function(resposta) {
				$('[data-js="mensagem-de-validacao"]').hide();

				if (resposta.autenticado === false) {
					$('[data-js="mensagem-de-validacao"]').show().text(resposta.mensagem);
					return;
				}

				sessaoDeUsuario.definirId(resposta.id_do_colaborador);
				buscarColaboradorView.exibir();
			});
		});
	}

	return loginView;
});
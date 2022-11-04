define([
	'text!app/cadastroDeColaboradores/formularioTemplate.html'
], function(cadastroTemplate) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;
		_sandbox.exibirTemplateEm('#conteudo', cadastroTemplate);
		$('#conteudo').on('focusout', 'input[id="idDiscord"]', validarUserIdDiscord);
	};

	function validarUserIdDiscord () {
		var userIdDiscord = $('#idDiscord').val();
		var chaveDiscord = ''
		$.ajax({
			beforeSend: function(request) {
				request.setRequestHeader("Authorization", 'Bot' + chaveDiscord);
			},
			dataType: "json",
			url: 'https://discord.com/api/v10/users/' + userIdDiscord,
			success: function(data) {
				// Se deu certo
			},
			statusCode: {
				404: function() {
				  // Se deu errado
				}
			  }
		});
	}

	self.finalizar = function() {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

    return self;
});
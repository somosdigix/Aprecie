define([
	'text!app/cadastroDeColaboradores/formularioTemplate.html'
], function(cadastroTemplate) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;
		_sandbox.exibirTemplateEm('#conteudo', cadastroTemplate);
		$("#conteudo").on("click", 'button[data-js="SalvarColaborador"]', validardataDeNascimento)
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

	function validardataDeNascimento(){
		var data = new Date($("#dataDeNascimento").val().replace(/-/g, '/'));
		var dataAtual= new Date();
		dataAtual.setHours(0,0,0,0);

		console.log(dataAtual);
		console.log(data);

		var mensagem = $('#alert-data');
		console.log(mensagem);
		if (data<dataAtual){
			console.log("Data Válida");
			mensagem.text("Data válida");
			mensagem.removeClass("erro")
			mensagem.addClass("sucesso")
			
			return true;
		} else {
			console.log("Data Inválida");
			mensagem.text("Data inválida");
			mensagem.removeClass("sucesso")
			mensagem.addClass("erro")

			return false;
		}
	}

    return self;
});
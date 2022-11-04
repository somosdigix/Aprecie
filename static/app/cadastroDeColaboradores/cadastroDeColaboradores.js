define([
	'text!app/cadastroDeColaboradores/formularioTemplate.html',
	'growl'
], function (cadastroTemplate,
	growl) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;
		_sandbox.exibirTemplateEm('#conteudo', cadastroTemplate);
		$('#conteudo').on('focusout', 'input[id="idDiscord"]', validarUserIdDiscord);
		$("#salvarColaborador").click(function () {
			salvarColaborador();
		});
	};

	function salvarColaborador() {
		var nome = $("#nomeColaborador").val();
		var cpf = $("#cpf").val();
		var dataNascimento = $("#dataDeNascimento").val();
		var idDiscord = $("#idDiscord").val();
		var data = {
			"colaboradores": [{
				"nome": nome,
				"cpf": cpf,
				"data_de_nascimento": dataNascimento,
				"usuario_id_do_chat": idDiscord
			}]	
		};

		$.post("/colaborador/", data, function () {
			growl.deSucesso().exibir("Reconhecimento realizado com sucesso.");
		}).fail(function () {
			growl.deErro().exibir(erro.message);
		});


	}

	function validarUserIdDiscord() {
		var userIdDiscord = $('#idDiscord').val();
		var chaveDiscord = ''
		$.ajax({
			beforeSend: function (request) {
				request.setRequestHeader("Authorization", 'Bot' + chaveDiscord);
			},
			dataType: "json",
			url: 'https://discord.com/api/v10/users/' + userIdDiscord,
			success: function (data) {
				// Se deu certo
			},
			statusCode: {
				404: function () {
					// Se deu errado
				}
			}
		});
	}

	self.finalizar = function () {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	return self;
});
define([
	'jquery',
	'handlebars',
	'jquery.blockui',
	'localizacao'
], function($, Handlebars, blockUI) {
	'use strict';

	var configuracoes = {};
	var _ehDebug = false;

	configuracoes.configurarErros = function() {
		window.onerror = function(error) {
			if (error.indexOf('ViolacaoDeRegra') === -1 &&
				error.indexOf('ErroInesperado') === -1)
				return;

			require(['growl'], function(growl) {
				var mensagemDeErro = error
					.replace('Uncaught ViolacaoDeRegra: ', '')
					.replace('ViolacaoDeRegra: ', '')
					.replace('Uncaught ErroInesperado: ', '')
					.replace('ErroInesperado: ', '');

				growl.deErro().exibir(mensagemDeErro);
			});
		};
	};

	configuracoes.configurarErrosDeRequisicao = function() {
		var tempo;

		$(document)
			.ajaxStart(function() {
				tempo = setTimeout(function() {
					$.blockUI({
						message: 'Carregando, aguarde...'
					});
				}, 100);
			})
			.ajaxComplete(desbloquearInterface)
			.ajaxError(function(evento, jqueryRequest) {
				var statusCode = jqueryRequest.status;
				desbloquearInterface();

				if (statusCode === 500)
					throw new ErroInesperado('Ih, deu ruim! Por favor, avise o RH. :(');

				var erro = JSON.parse(jqueryRequest.responseText);

				throw new ViolacaoDeRegra(erro.mensagem);
			});

		function desbloquearInterface() {
			$.unblockUI();
			clearTimeout(tempo);
		}
	};

	configuracoes.registrarHelpersGlobaisDoHandlebars = function() {
		var localizacao = require('localizacao');

		Handlebars.registerHelper('foto', function(base64) {
			return base64 ? base64 : 'static/img/sem-foto.png';
		});

		Handlebars.registerHelper('emDataLegivel', function(data) {
			return localizacao.formatarData(data);
		});
	};

	configuracoes.configurarDebug = function(ehDebug) {
		_ehDebug = ehDebug;
	};

	configuracoes.ehDebug = function() {
		return _ehDebug;
	};

	return configuracoes;
});
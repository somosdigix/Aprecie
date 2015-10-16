define([
	'jquery',
	'handlebars'
], function($, Handlebars) {
	'use strict';
	
	var configuracoes = {};
	var _ehDebug = false;

	configuracoes.configurarErros = function() {
		window.onerror = function(error) {
			if (error.indexOf('ViolacaoDeRegra') === -1)
				return;

			require(['growl'], function(growl) {
				var mensagemDeErro = error
					.replace('ViolacaoDeRegra: ', '')
					.replace('Uncaught ViolacaoDeRegra: ', '');
					
				growl.deErro().exibir(mensagemDeErro);
			});
		};
	};

	configuracoes.configurarErrosDeRequisicao = function() {
		$(document).ajaxError(function(evento, jqueryRequest) {
			var statusCode = jqueryRequest.status;
			var erro = JSON.parse(jqueryRequest.responseText);

			if (statusCode === 500)
				throw new Error(erro.mensagem);

			throw new ViolacaoDeRegra(erro.mensagem);
		});
	};

	configuracoes.registrarHelpersGlobaisDoHandlebars = function() {
		Handlebars.registerHelper('foto', function(base64) {
			return base64 ? base64 : 'static/img/sem-foto.png';
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
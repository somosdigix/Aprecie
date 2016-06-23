define([
	'jquery',
	'handlebars',
	'moment'
], function($, Handlebars, moment) {
	'use strict';

	var configuracoes = {};
	var _ehDebug = false;

	configuracoes.configurarErros = function() {
		window.onerror = function(mensagem, fonte, linha, coluna, erro) {
			if (mensagem.indexOf('ViolacaoDeRegra') === -1 &&
				mensagem.indexOf('ErroInesperado') === -1)
				return;

			require(['growl'], function(growl) {
				growl.deErro().exibir(erro.message);
			});
		};
	};

	configuracoes.configurarErrosDeRequisicao = function() {
		var tempo;

		$(document)
			.ajaxStart(function() {
				tempo = setTimeout(function() {
					$('div[data-js="carregando"]').removeClass('disabled').addClass('active');
				}, 250);
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
			$('div[data-js="carregando"]').removeClass('active').addClass('disabled');
			clearTimeout(tempo);
		}
	};

	configuracoes.registrarHelpersGlobaisDoHandlebars = function() {
		Handlebars.registerHelper('foto', function(id, usar_miniatura) {
			var eh_miniatura = eh_miniatura ? 1 : 0;
			var url = '../login/foto/' + id + '?eh_miniatura=' + eh_miniatura;
			return url;
		});

		Handlebars.registerHelper('emDataLegivel', function(data) {
			return moment(data, 'YYYY-MM-DD').format('DD/MM/YYYY')
		});
	};

	configuracoes.configurarDebug = function() {
		_ehDebug = document.getElementById('ehDebug').value === 'True';
	};

	configuracoes.ehDebug = function() {
		return _ehDebug;
	};

	return configuracoes;
});
define([
	'jquery',
	'handlebars',
	'jquery.blockui',
	"globalize",

	// CLDR content.
	'json!cldr-data/supplemental/likelySubtags.json',
	'json!cldr-data/main/pt/numbers.json',
	'json!cldr-data/supplemental/numberingSystems.json',
	'json!cldr-data/main/pt/ca-gregorian.json',
	'json!cldr-data/main/pt/timeZoneNames.json',
	'json!cldr-data/supplemental/timeData.json',
	'json!cldr-data/supplemental/weekData.json',

	// Extend Globalize with Date and Number modules.
	"globalize/date",
	"globalize/number"

], function($, Handlebars, blockUI, Globalize, likelySubtags, ptNumbers, numberingSystems, ptGregorian, ptTimezones, timeData, weekData) {
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
		Globalize.load(likelySubtags, ptNumbers, numberingSystems, ptGregorian, ptTimezones, timeData, weekData);
		var localidade = Globalize('pt');

		Handlebars.registerHelper('foto', function(base64) {
			return base64 ? base64 : 'static/img/sem-foto.png';
		});

		Handlebars.registerHelper('emDataLegivel', function(data) {
			return localidade.formatDate(localidade.parseDate(data, {raw: 'yyyy-MM-dd'}));
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
define([
	'jquery',
	'handlebars'
], function($, Handlebars) {
	'use strict';

	var template = {};

	template.exibir = function(conteudo, modelo) {
		template.exibirEm('#conteudo', conteudo, modelo);
	};

	template.exibirEm = function(container, conteudo, modelo) {
		var conteudoCompilado = Handlebars.compile(conteudo);
		$(container).empty().append(conteudoCompilado(modelo));
	};

	template.acrescentarEm = function(container, conteudo, modelo) {
		var conteudoCompilado = Handlebars.compile(conteudo);
		$(container).append(conteudoCompilado(modelo));
	};

	template.exibirComRequire = function(container, nomeDoTemplate, dados) {
		var acao = function(resolver) {
			var urlDoTemplate = 'text!partials/' + nomeDoTemplate;

			require([
				urlDoTemplate,
				'handlebars'
			], function(template, Handlebars) {
				var jContainer = $(container);
				var conteudo = Handlebars.compile(template)(dados);

				jContainer.append(conteudo);
				resolver();
			});
		};

		return new Promise(acao);
	}

	return template;
});
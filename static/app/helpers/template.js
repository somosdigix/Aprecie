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

	return template;
});
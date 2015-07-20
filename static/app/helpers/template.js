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
		$(container).html(conteudoCompilado(modelo));
	};

	return template;
});
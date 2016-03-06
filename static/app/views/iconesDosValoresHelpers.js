define([
	'handlebars'
], function(Handlebars) {
	'use strict';
	
	Handlebars.registerHelper('iconeDoValor', function(valor) {
		var urlBase = '../static/img/';
		var valor = valor.nome.toLocaleLowerCase();

		return urlBase + valor + '.png';
	});
});
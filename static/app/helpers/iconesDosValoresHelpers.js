define([
	'handlebars'
], function(Handlebars) {
	'use strict';

	var icones = {
		'inquietude': 'inquietude.png',
		'responsabilidade': 'responsabilidade.png',
		'resultado': 'resultado.png',
		'alegria': 'alegria.png',
		'relacionamento': 'relacionamento.png',
		'segurança': 'seguranca.png',
		'colaboração': 'colaboracao.png'
	};

	Handlebars.registerHelper('iconeDoValor', function(valor) {
		var urlBase = '../static/img/';
		var nomeDoValor = valor.nome ? valor.nome.toLocaleLowerCase() : valor.toLocaleLowerCase();

		return urlBase + icones[nomeDoValor];
	});
});

define([
	'handlebars'
], function(Handlebars) {
	'use strict';
	
	var iconesDosValores = {
		'Inquietude': '../static/img/inquietude.png',
		'Responsabilidade': '../static/img/responsabilidade.png',
		'Resultado': '../static/img/resultado.png',
		'Transparência': '../static/img/transparencia.png',
		'Alegria': '../static/img/alegria.png',
		'Excelência': '../static/img/excelencia.png',
		'Colaboração': '../static/img/colaboracao.png'
	};

	Handlebars.registerHelper('iconeDoValor', function(valor) {
		return iconesDosValores[valor.nome];
	});
});
define([
	'jquery',
	'template',
	'text!partials/reconhecimentosPorValorTemplate.html'
], function($, template, reconhecimentosPorValorTemplate) {
	'use strict';

	var reconhecimentosPorValorView = {};

	reconhecimentosPorValorView.exibir = function(valorId) {
		console.log(valorId);
		template.exibir(reconhecimentosPorValorTemplate);
	};

	return reconhecimentosPorValorView;
});
define([
	'jquery',
	'handlebars',
	'text!partials/reconhecimentosPorReconhecedorTemplate.html'
], function($, Handlebars, reconhecimentosPorReconhecedorTemplate) {
	'use strict';

	var reconhecimentosPorReconhecedorView = {};

	reconhecimentosPorReconhecedorView.exibir = function(colaboradorId) {
		var data = {
			id_do_reconhecido: colaboradorId
		};

		var template = Handlebars.compile(reconhecimentosPorReconhecedorTemplate);

		$.getJSON('/reconhecimentos/por_reconhecedor/', data, function(reconhecimentosPorReconhecedor) {
			reconhecimentosPorReconhecedor.map(function(reconhecimento) {
				var secaoDoValor = $('section[data-valor-id="' + reconhecimento.id_do_valor + '"]');
				secaoDoValor.append(template(reconhecimento));
			});
		});
	};

	return reconhecimentosPorReconhecedorView;
});
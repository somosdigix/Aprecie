define([
	'jquery',
	'template',
	'text!partials/reconhecimentosPorReconhecedorTemplate.html'
], function($, template, reconhecimentosPorReconhecedorTemplate) {
	'use strict';

	var reconhecimentosPorReconhecedorView = {};

	reconhecimentosPorReconhecedorView.exibir = function(colaboradorId) {
		var data = {
			id_do_reconhecido: colaboradorId
		};

		$.getJSON('/reconhecimentos/por_reconhecedor/', data, function(reconhecimentosPorReconhecedor) {
			reconhecimentosPorReconhecedor.map(function(reconhecimento) {
				var secaoDoValor = 'section[data-valor-id="' + reconhecimento.id_do_valor + '"]';
				template.acrescentarEm(secaoDoValor, reconhecimentosPorReconhecedorTemplate, reconhecimento);
			});
		});
	};

	return reconhecimentosPorReconhecedorView;
});
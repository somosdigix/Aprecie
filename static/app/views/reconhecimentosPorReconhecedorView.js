define([
	'jquery',
	'template',
	'text!partials/reconhecimentosPorReconhecedorTemplate.html'
], function($, template, reconhecimentosPorReconhecedorTemplate) {
	'use strict';

	var reconhecimentosPorReconhecedorView = {};

	reconhecimentosPorReconhecedorView.exibir = function(colaboradorId) {
		$.getJSON('/reconhecimentos/por_reconhecedor/' + colaboradorId, {}, function(resultado) {
			resultado.reconhecedores.map(function(reconhecimento) {
				var secaoDoValor = 'section[data-valor-id="' + reconhecimento.valor__id + '"]';
				template.acrescentarEm(secaoDoValor, reconhecimentosPorReconhecedorTemplate, reconhecimento);
			});
		});
	};

	return reconhecimentosPorReconhecedorView;
});
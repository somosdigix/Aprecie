define([
	'jquery',
	'template',
	'text!partials/reconhecimentosTemplate.html'
], function($, template, reconhecimentosTemplate) {
	'use strict';

	var reconhecimentosPorValorView = {};

	reconhecimentosPorValorView.exibir = function(colaboradorId, valorId) {	
		$('#conteudo').off()
			.on('click', 'a[data-js="voltar-ao-perfil"]', function () {
				voltarParaPerfil(colaboradorId);
			});

		$.getJSON('/reconhecimentos/' + colaboradorId + '/' + valorId, {}, function (resposta) {
			template.exibir(reconhecimentosTemplate, resposta);
		});
	}

	function voltarParaPerfil(reconhecidoId) {
		require(['roteador'], function(roteador) {
			roteador.navegarPara('/perfil/' + reconhecidoId);
		});
	}

	return reconhecimentosPorValorView;
});
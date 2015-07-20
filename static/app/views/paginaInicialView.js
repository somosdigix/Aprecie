define([
	'jquery',
	'template',
	'text!partials/paginaInicialTemplate.html'
], function($, template, paginaInicialTemplate) {
	'use strict';
	
	var paginaInicialView = {};

	paginaInicialView.exibir = function() {
		$.get('/reconhecimentos/ultimos/', function(ultimosReconhecimentos) {
			template.exibir(paginaInicialTemplate, ultimosReconhecimentos);

			$('#conteudo').off().on('click', 'strong[data-js="ir-ao-perfil"]', irAoPerfil);
		});
	};

	function irAoPerfil() {
		var reconhecidoId = $(this).data('id');

		require(['app/views/perfilView'], function(perfilView) {
			perfilView.exibir(reconhecidoId);
		});
	}

	return paginaInicialView;
});
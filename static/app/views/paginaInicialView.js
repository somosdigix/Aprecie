define([
	'jquery',
	'handlebars',
	'text!partials/paginaInicialTemplate.html'
], function($, Handlebars, paginaInicialTemplate) {
	var paginaInicialView = {};

	paginaInicialView.exibir = function() {
		var template = Handlebars.compile(paginaInicialTemplate);

		$.get('/reconhecimentos/ultimos/', function(ultimosReconhecimentos) {
			$('#conteudo')
				.empty()
				.html(template(ultimosReconhecimentos))
				.on('click', 'strong[data-js="ir-ao-perfil"]', irAoPerfil);
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
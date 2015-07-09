define([
	'jquery',
	'handlebars',
	'text!partials/paginaInicialTemplate.html',
	'app/models/sessaoDeUsuario'
], function($, Handlebars, paginaInicialTemplate, sessaoDeUsuario) {
	var paginaInicialView = {};

	paginaInicialView.exibir = function() {
		var template = Handlebars.compile(paginaInicialTemplate);
		$('#conteudo').empty().html(template(sessaoDeUsuario));

		$('#conteudo').off().on('click', 'button[data-js="buscar"]', buscar);
	};

	function buscar() {
		require([
			'app/views/buscarColaboradorView'
		], function(buscarColaboradorView) {
			buscarColaboradorView.exibir();
		});
	}

	return paginaInicialView;
});
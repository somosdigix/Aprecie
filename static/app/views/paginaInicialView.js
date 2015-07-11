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
	};

	return paginaInicialView;
});
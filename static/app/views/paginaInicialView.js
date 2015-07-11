define([
	'jquery',
	'handlebars',
	'text!partials/paginaInicialTemplate.html'
], function($, Handlebars, paginaInicialTemplate) {
	var paginaInicialView = {};

	paginaInicialView.exibir = function() {
		var template = Handlebars.compile(paginaInicialTemplate);

		$.get('/reconhecimentos/ultimos/', function(ultimosReconhecimentos) {
			$('#conteudo').empty().html(template(ultimosReconhecimentos));
		});
	};

	return paginaInicialView;
});
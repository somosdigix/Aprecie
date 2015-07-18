define([
	'jquery',
	'handlebars'
], function($, Handlebars) {
	var template = {
		inserir: function(conteudo, modelo) {
			var conteudoCompilado = Handlebars.compile(conteudo);
			$("#conteudo").html(conteudoCompilado(modelo));
		}
	};

	return template;
});
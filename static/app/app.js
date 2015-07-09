var configuracoes = {
	baseUrl: '',

	paths: {
		'text': 'app/lib/requirejs-text/text',
		'jquery': 'app/lib/jquery/dist/jquery',
		'jquery-ui': 'app/lib/jquery-ui/jquery-ui',
		'handlebars': 'app/lib/handlebars/handlebars.amd',
		'configuracoes': 'app/configuracoes',
		'jquery.inputmask': 'app/lib/jquery.inputmask/dist/jquery.inputmask.bundle'
	}
};

require.config(configuracoes);

require([
	'app/views/loginView'
], function(loginView) {
	'use strict';

	loginView.exibir();

	window.onerror = function(error) {
		if (error.indexOf('ViolacaoDeRegra') === -1)
			return;

		var mensagemDeErro = error.replace('Uncaught ViolacaoDeRegra: ', '');
		console.error(mensagemDeErro);
	};
});
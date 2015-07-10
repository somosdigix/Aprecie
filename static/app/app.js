var configuracoes = {
	baseUrl: 'static',

	deps: ['app/excecoes/violacaoDeRegra'],

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
	'configuracoes',
	'app/views/loginView'
], function(configuracoes, loginView) {
	'use strict';

	configuracoes.configurarErros();
	configuracoes.configurarErrosDeRequisicao();
	
	loginView.exibir();
});
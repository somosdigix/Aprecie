var configuracoes = {
	baseUrl: 'static',

	deps: [
		'app/excecoes/violacaoDeRegra',
		'app/excecoes/erroInesperado'
	],

	paths: {
		'text': 'app/lib/requirejs-text/text',
		'jquery': 'app/lib/jquery/dist/jquery',
		'jquery-ui': 'app/lib/jquery-ui/jquery-ui',
		'jquery.inputmask': 'app/lib/jquery.inputmask/dist/jquery.inputmask.bundle',
		'jquery.blockui': 'app/lib/blockUI/jquery.blockUI',
		'handlebars': 'app/lib/handlebars/handlebars.amd',
		'director': 'app/lib/director/build/director',
		'roteador': 'app/roteador',
		'configuracoes': 'app/configuracoes',
		'template': 'app/helpers/template',
		'cookie': 'app/helpers/cookie',
		'growl': 'app/helpers/growl',
		'sessaoDeUsuario': 'app/models/sessaoDeUsuario'
	},

	shim: {
		'jquery': {
			exports: '$'
		},

		'jquery-ui': {
			deps: ['jquery'],
			exports: '$'
		},

		'jquery.inputmask': {
			deps: ['jquery'],
			exports: '$'
		},

		'director': {
			exports: 'Router'
		}
	}
};

var ehDebug = document.getElementById('ehDebug').value === 'True';
configuracoes.urlArgs = ehDebug ? 'antiCache=' + (new Date()).getTime() : 'antiCache=3';

require.config(configuracoes);

require([
	'roteador',
	'configuracoes'
], function(roteador, configuracoes) {
	'use strict';

	roteador.configurar();
	configuracoes.configurarDebug(ehDebug);
	configuracoes.configurarErros();
	configuracoes.configurarErrosDeRequisicao();
	configuracoes.registrarHelpersGlobaisDoHandlebars();

	if (roteador.paginaAtual() === '')
		roteador.navegarPara('/login');
});
var configuracoes = {
	baseUrl: '../static',

	deps: [
		'app/excecoes/violacaoDeRegra',
		'app/excecoes/erroInesperado',
		'app/helpers/string',
	],

	paths: {
		'text': 'lib/requirejs-text/text',
		'jquery': 'lib/jquery/dist/jquery',
		'jquery-ui': 'lib/jquery-ui/jquery-ui',
		'jquery.inputmask': 'lib/jquery.inputmask/dist/jquery.inputmask.bundle',
		'jquery.blockui': 'lib/blockUI/jquery.blockUI',
		'handlebars': 'lib/handlebars/handlebars.amd',
		'director': 'lib/director/build/director',
		'sandbox': 'app/sandbox',
		'gerenciadorDeModulos': 'app/gerenciadorDeModulos',
		'roteador': 'app/roteador',
		'localizacao': 'app/localizacao',
		'configuracoes': 'app/configuracoes',
		'template': 'app/helpers/template',
		'cookie': 'app/helpers/cookie',
		'growl': 'app/helpers/growl',
		'sessaoDeUsuario': 'app/models/sessaoDeUsuario',
		"cldr": "lib/cldrjs/dist/cldr",
		"cldr-data": "lib/cldr-data",
		"json": "lib/requirejs-plugins/src/json",
		"globalize": "lib/globalize/dist/globalize"
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

// TODO: Automatizar essa feiura na build
var ehDebug = document.getElementById('ehDebug').value === 'True';
configuracoes.urlArgs = ehDebug ? 'antiCache=' + (new Date()).getTime() : 'antiCache=6';

require.config(configuracoes);

require([
	'roteador',
	'configuracoes',

	// TODO: Colocar no "deps" do RequireJS
	'jquery.inputmask'
], function(roteador, configuracoes) {
	'use strict';

	roteador.configurar();
	configuracoes.configurarDebug(ehDebug);
	configuracoes.configurarErros();
	configuracoes.configurarErrosDeRequisicao();
	configuracoes.registrarHelpersGlobaisDoHandlebars();

	if (roteador.paginaAtual() === '')
		roteador.navegarPara('/paginaInicial');
});
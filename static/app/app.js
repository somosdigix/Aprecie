var configuracoes = {
	baseUrl: 'static',

	deps: ['app/excecoes/violacaoDeRegra'],

	paths: {
		'text': 'app/lib/requirejs-text/text',
		'jquery': 'app/lib/jquery/dist/jquery',
		'jquery-ui': 'app/lib/jquery-ui/jquery-ui',
		'jquery.inputmask': 'app/lib/jquery.inputmask/dist/jquery.inputmask.bundle',
		'handlebars': 'app/lib/handlebars/handlebars.amd',
		'director': 'app/lib/director/build/director',
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

require.config(configuracoes);

require([
	'app/rotas',
	'configuracoes',
	'app/servicos/servicoDeAutenticacao',
	'app/views/loginView',
	'app/views/toolbarView',
	'app/views/paginaInicialView'
], function(rotas, configuracoes, servicoDeAutenticacao, loginView, toolbarView, paginaInicialView) {
	'use strict';

	rotas.configurar();
	configuracoes.configurarErros();
	configuracoes.configurarErrosDeRequisicao();
	configuracoes.registrarHelpersGlobaisDoHandlebars();

	if (servicoDeAutenticacao.jaEstaAutenticado()) {
		servicoDeAutenticacao.atualizarSessaoDeUsuario();
		toolbarView.exibir(paginaInicialView.exibir);

		return;
	}

	loginView.exibir();
});
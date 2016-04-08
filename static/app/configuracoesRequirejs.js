window.configuracoesRequirejs = (function() {
	// TODO: Automatizar essa feiura na build
	var ehDebug = document.getElementById('ehDebug').value === 'True';
	var deveUsarAntiCache = ehDebug ? 'antiCache=' + (new Date()).getTime() : 'antiCache=8';

	return {
		urlArgs: deveUsarAntiCache,
		baseUrl: '/static',

		deps: [
			'semantic',
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
			'semantic': 'tema/dist/semantic',
			'handlebars': 'lib/handlebars/handlebars.amd',
			'director': 'lib/director/build/director',
			'sandbox': 'app/sandbox',
			'gerenciadorDeModulos': 'app/gerenciadorDeModulos',
			'roteador': 'app/roteador',
			'configuracoes': 'app/configuracoes',
			'template': 'app/helpers/template',
			'cookie': 'app/helpers/cookie',
			'growl': 'app/helpers/growl',
			'sessaoDeUsuario': 'app/models/sessaoDeUsuario',
			'moment': 'lib/moment/moment'
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

			'semantic': {
				deps: ['jquery']
			},

			'director': {
				exports: 'Router'
			}
		}
	};
})();
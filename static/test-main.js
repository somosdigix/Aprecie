var allTestFiles = [];
var TEST_REGEXP = /(spec|test)\.js$/i;

var pathToModule = function(path) {
	return path.replace(/^\/base\//, '').replace(/\.js$/, '');
};

Object.keys(window.__karma__.files).forEach(function(file) {
	if (TEST_REGEXP.test(file)) {
		// Normalize paths to RequireJS module names.
		allTestFiles.push(pathToModule(file));
	}
});

require.config({
	// Karma serves files under /base, which is the basePath from your config file
	baseUrl: '/base',

	// dynamically load all test files
	deps: allTestFiles,

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
		}
	},

	// we have to kickoff jasmine, as it is asynchronous
	callback: window.__karma__.start
});
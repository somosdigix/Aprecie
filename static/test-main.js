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
		'text': 'app/lib/requirejs-text/text',
		'jquery': 'app/lib/jquery/dist/jquery',
		'jquery-ui': 'app/lib/jquery-ui/jquery-ui',
		'jquery.inputmask': 'app/lib/jquery.inputmask/dist/jquery.inputmask.bundle',
		'handlebars': 'app/lib/handlebars/handlebars.amd',
		'configuracoes': 'app/configuracoes',
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
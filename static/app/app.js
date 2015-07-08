var configuracoes = {
	baseUrl: '',

	paths: {
		'text': 'app/lib/requirejs-text/text',
		'jquery': 'app/lib/jquery/dist/jquery',
		'jquery-ui': 'app/lib/jquery-ui/jquery-ui',
	'handlebars': 'app/lib/handlebars/handlebars.amd'
	}
};

require.config(configuracoes);

require([
'app/views/loginView'
], function(loginView) {
	'use strict';

	loginView.exibir(1);
});
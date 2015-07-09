define(function() {
	var configuracoes = {};

	configuracoes.ehDebug = function() {
		return window.location.toString().indexOf('?debug=true') > -1;
	};

	return configuracoes;
});
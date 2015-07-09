define(function() {
	var configuracoes = {};

	configuracoes.configurarErros = function() {
		window.onerror = function(error) {
			if (error.indexOf('ViolacaoDeRegra') === -1)
				return;

			require(['app/helpers/growl'], function(growl) {
				var mensagemDeErro = error.replace('Uncaught ViolacaoDeRegra: ', '');
				growl.exibir(mensagemDeErro);
			});
		};
	};

	configuracoes.ehDebug = function() {
		return window.location.toString().indexOf('?debug=true') > -1;
	};

	return configuracoes;
});
require.config(window.configuracoesRequirejs);

require([
	'roteador',
	'configuracoes',

	// TODO: Colocar no "deps" do RequireJS
	'jquery.inputmask'
], function(roteador, configuracoes) {
	'use strict';

	roteador.configurar();
	configuracoes.configurarDebug();
	configuracoes.configurarErros();
	configuracoes.configurarErrosDeRequisicao();
	configuracoes.registrarHelpersGlobaisDoHandlebars();
});
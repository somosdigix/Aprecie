require.config(window.configuracoesRequirejs);

require([
	'configuracoes',
	'app/login/controller',
	'jquery.inputmask'
], function(configuracoes, controller) {
	configuracoes.configurarDebug(ehDebug);
	configuracoes.configurarErros();
	configuracoes.configurarErrosDeRequisicao();

	controller.exibir();
});
require.config(window.configuracoesRequirejs);

require([
  'core',
  'roteador',
	'configuracoes',
	'jquery.inputmask'
], function(Core, roteador, configuracoes) {
 //  roteador.configurar();
	// configuracoes.configurarDebug();
	// configuracoes.configurarErros();
	// configuracoes.configurarErrosDeRequisicao();

  // roteador.navegarPara('/');

  Core.registrar('login', function() {
  });
});
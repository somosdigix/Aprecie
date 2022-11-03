define([
	"sessaoDeUsuario",
],
	function(sessaoDeUsuario) {
'use strict';

var recursosHumanosHelper = {};

recursosHumanosHelper.ehRecursosHumanos = function() {
	if (!sessaoDeUsuario.recursos_humanos) {
		require(["growl"], function (growl) {
			growl.deErro().exibir("Você não é do RH");
			return false;
		});
	} else {
		return sessaoDeUsuario.recursos_humanos;
	}
};

recursosHumanosHelper.mostrarConteudoSeForRecursosHumanos = function(conteudo) {
	if (sessaoDeUsuario.recursos_humanos === false) {
		$(conteudo).hide();
	} else {
		$(conteudo).show();
	}
}

return recursosHumanosHelper;
});
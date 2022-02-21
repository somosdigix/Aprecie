define([
    "sessaoDeUsuario",
],
    function(sessaoDeUsuario) {
	'use strict';

	var administradorHelper = {};

	administradorHelper.ehAdministrador = function() {
		if (!sessaoDeUsuario.administrador) {
			require(["growl"], function (growl) {
				growl.deErro().exibir("Você não é administrador");
				return false;
			});
		} else {
			return sessaoDeUsuario.administrador;
		}
	};

	administradorHelper.mostrarConteudoSeForAdministrador = function(conteudo) {
		if (sessaoDeUsuario.administrador === false) {
			$(conteudo).hide();
		} else {
			$(conteudo).show();
		}
	}

	return administradorHelper;
});
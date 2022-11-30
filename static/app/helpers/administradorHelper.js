define([
	"sessaoDeUsuario",
	"template",
	'text!app/perfil/menuAdministradorTemplate.html'
],
	function (sessaoDeUsuario, template, menu) {
		'use strict';

		var administradorHelper = {};

		administradorHelper.ehAdministrador = function () {
			if (!sessaoDeUsuario.administrador) {
				require(["growl"], function (growl) {
					growl.deErro().exibir("Você não é administrador");
					return false;
				});
			} else {
				return sessaoDeUsuario.administrador;
			}
		};

		administradorHelper.mostrarConteudoSeForAdministrador = function (conteudo) {
			if (sessaoDeUsuario.administrador === true) {
				template.exibirEm(conteudo, menu);
			}
		}

		return administradorHelper;
	});
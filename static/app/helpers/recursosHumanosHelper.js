define([
	"sessaoDeUsuario",
	"template",
	'text!app/perfil/menuRHTemplate.html'
],
	function (sessaoDeUsuario, template, menu) {
		'use strict';

		var recursosHumanosHelper = {};

		recursosHumanosHelper.ehRecursosHumanos = function () {
			if (!sessaoDeUsuario.recursos_humanos) {
				require(["growl"], function (growl) {
					growl.deErro().exibir("Você não é do RH");
					return false;
				});
			} else {
				return sessaoDeUsuario.recursos_humanos;
			}
		};

		recursosHumanosHelper.mostrarConteudoSeForRecursosHumanos = function (conteudo) {
			if (sessaoDeUsuario.recursos_humanos === true) {
				template.exibirEm(conteudo, menu);
			}
		}

		return recursosHumanosHelper;
	});
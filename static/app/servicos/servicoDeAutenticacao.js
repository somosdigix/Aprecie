define([
	'sessaoDeUsuario',
	'cookie'
], function(sessaoDeUsuario, cookie) {
	 'use strict';

	 var servicoDeAutenticacao = {};

	 servicoDeAutenticacao.autenticar = function(colaborador) {
	 	sessaoDeUsuario.preencherDados(colaborador);
	 	cookie.criar('colaborador', JSON.stringify(colaborador));
	 };

	 servicoDeAutenticacao.jaEstaAutenticado = function() {
	 	return document.cookie.indexOf('colaborador@aprecie.me') > -1;
	 };

	 servicoDeAutenticacao.atualizarSessaoDeUsuario = function() {
	 	var colaborador = JSON.parse(cookie.obter('colaborador'));
	 	sessaoDeUsuario.preencherDados(colaborador);
	 };

	 return servicoDeAutenticacao;
});
define([
	'sessaoDeUsuario'
], function(sessaoDeUsuario) {
	 'use strict';

	 var servicoDeAutenticacao = {};

	 servicoDeAutenticacao.autenticar = function(colaborador) {
	 	sessaoDeUsuario.preencherDados(colaborador);
	 	document.cookie = 'colaborador@aprecie.me=' + JSON.stringify(colaborador);
	 };

	 servicoDeAutenticacao.jaEstaAutenticado = function() {
	 	return document.cookie.indexOf('colaborador@aprecie.me') > -1;
	 };

	 servicoDeAutenticacao.atualizarSessaoDeUsuario = function() {
	 	var cookies = document.cookie.split('; ');
	 	var cookieDeAutenticacao = cookies.filter(function(cookie) {
	 		return cookie.indexOf('colaborador@aprecie.me') > -1;
	 	})[0];
	 	var colaborador = JSON.parse(cookieDeAutenticacao.replace('colaborador@aprecie.me=', ''));

	 	sessaoDeUsuario.preencherDados(colaborador);
	 };

	 return servicoDeAutenticacao;
});
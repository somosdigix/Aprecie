define([
	'sessaoDeUsuario',
	'cookie'
], function(sessaoDeUsuario, cookie) {
	 'use strict';

	 var servicoDeAutenticacao = {};

	 servicoDeAutenticacao.autenticar = function(colaborador) {
	 	sessaoDeUsuario.preencherDados(colaborador);
	 	cookie.criar('id', colaborador.id_do_colaborador);
	 	cookie.criar('nome', colaborador.nome_do_colaborador);
	 };

	 servicoDeAutenticacao.jaEstaAutenticado = function() {
	 	return document.cookie.indexOf('@aprecie.me') > -1;
	 };

	 servicoDeAutenticacao.atualizarSessaoDeUsuario = function() {
	 	if (!sessaoDeUsuario.estaVazia()) return;
	 	
	 	var colaborador = {};
	 	colaborador.id = cookie.obter('id');
	 	colaborador.nome = cookie.obter('nome');

	 	sessaoDeUsuario.preencherDados(colaborador);
	 };

	 return servicoDeAutenticacao;
});
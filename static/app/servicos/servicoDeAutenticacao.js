define([
	'sessaoDeUsuario',
	'app/helpers/cookie'
], function(sessaoDeUsuario, cookie) {
	'use strict';

	var servicoDeAutenticacao = {};

	servicoDeAutenticacao.autenticar = function(colaborador) {
		cookie.criar('id', colaborador.id_do_colaborador);
		cookie.criar('nome', colaborador.nome_do_colaborador);
		cookie.criar('administrador', colaborador.administrador);
	};

	servicoDeAutenticacao.jaEstaAutenticado = function() {
		return document.cookie.indexOf('@aprecie.me') > -1;
	};

	servicoDeAutenticacao.atualizarSessaoDeUsuario = function() {
		if (!sessaoDeUsuario.estaVazia()) return;

		var colaborador = {};
		colaborador.id_do_colaborador = cookie.obter('id');
		colaborador.nome_do_colaborador = cookie.obter('nome');
		colaborador.administrador = cookie.obter('administrador');

		sessaoDeUsuario.preencherDados(colaborador);
	};

	return servicoDeAutenticacao;
});
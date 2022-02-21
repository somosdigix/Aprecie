define([
	'jquery',
	'sessaoDeUsuario',
	'app/helpers/cookie'
], function($, sessaoDeUsuario, cookie) {
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

	servicoDeAutenticacao.validar = function() {
		if(this.jaEstaAutenticado()){
			var sessaoAtual = {
				'id': sessaoDeUsuario.id,
				'administrador': sessaoDeUsuario.administrador
			}
			$.post("/login/verificar_usuario/", sessaoAtual, function(usuario) {
				var usuarioValidado = JSON.parse(usuario.valido);
				if(!usuarioValidado){
					cookie.limpar();
					window.location = '/';
				}
			})
		};
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
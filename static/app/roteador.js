define([
	'director',
	'app/servicos/servicoDeAutenticacao'
], function(Router, servicoDeAutenticacao) {
	'use strict';

	var roteador = {};

	roteador.configurar = function() {
		var rotas = {
			'/login': [middlewareDeAutenticacao, middlewareDeToolbar, login],
			'/paginaInicial': [middlewareDeAutenticacao, middlewareDeToolbar, paginaInicial]
		};

		function login() {
			require(['app/views/loginView'], function(loginView) {
				loginView.exibir();
			});
		}

		function paginaInicial() {
			require(['app/views/paginaInicialView'], function(paginaInicialView) {
				paginaInicialView.exibir();
			});
		}

		var router = Router(rotas);
		router.init();
	};

	roteador.navegarPara = function(endereco) {
		window.location = '/#' + endereco;
	};

	roteador.paginaAtual = function() {
		var endereco = window.location.toString();
		var posicaoDaRota = endereco.indexOf('#') + 1;

		return endereco.substring(posicaoDaRota);
	}

	function middlewareDeAutenticacao() {
		if (roteador.paginaAtual() === '/login' && !servicoDeAutenticacao.jaEstaAutenticado())
			return true;

		if (!servicoDeAutenticacao.jaEstaAutenticado()) {
			roteador.navegarPara('/login');
			return false;
		}

		servicoDeAutenticacao.atualizarSessaoDeUsuario();
	}

	function middlewareDeToolbar() {
		require(['app/views/toolbarView'], function(toolbarView) {
			if (servicoDeAutenticacao.jaEstaAutenticado() && roteador.paginaAtual() !== '/login')
				toolbarView.exibir();
			else
				toolbarView.esconder();
		});
	}

	return roteador;
});
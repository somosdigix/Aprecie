define([
	'director',
	'app/servicos/servicoDeAutenticacao'
], function(Router, servicoDeAutenticacao) {
	'use strict';

	var roteador = {};

	roteador.configurar = function() {
		var rotas = {
			'/login': login,
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

	function middlewareDeAutenticacao() {
		if (!servicoDeAutenticacao.jaEstaAutenticado()) {
			roteador.navegarPara('/login');
			return false;
		}

		servicoDeAutenticacao.atualizarSessaoDeUsuario();
	}

	function middlewareDeToolbar() {
		require(['app/views/toolbarView'], function(toolbarView) {
			if (servicoDeAutenticacao.jaEstaAutenticado())
				toolbarView.exibir();
			else
				toolbarView.esconder();
		});
	}

	return roteador;
});
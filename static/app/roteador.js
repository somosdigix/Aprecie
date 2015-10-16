define([
	'director',
	'app/servicos/servicoDeAutenticacao'
], function(Router, servicoDeAutenticacao) {
	'use strict';

	var router;
	var roteador = {};

	roteador.configurar = function() {
		var rotas = {
			'/login': [middlewareDeAutenticacao, middlewareDeToolbar, login],
			'/paginaInicial': [middlewareDeAutenticacao, middlewareDeToolbar, paginaInicial],
			'/perfil/:colaboradorId': [middlewareDeAutenticacao, middlewareDeToolbar, perfil],
			'/reconhecimentosPorValor/:colaboradorId/:valorId': [middlewareDeAutenticacao, middlewareDeToolbar, reconhecimentosPorValor]
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

		function perfil(colaboradorId) {
			require(['app/views/perfilView'], function(perfilView) {
				perfilView.exibir(parseInt(colaboradorId));
			});
		}

		function reconhecimentosPorValor(colaboradorId, valorId) {
			require(['app/views/reconhecimentosPorValorView'], function(reconhecimentosPorValorView) {
				reconhecimentosPorValorView.exibir(parseInt(colaboradorId), parseInt(valorId));
			});
		}

		router = Router(rotas);
		router.init();
	};

	roteador.navegarPara = function(endereco) {
		window.location = '/#' + endereco;
	};

	roteador.paginaAtual = function() {
		var endereco = window.location.toString();
		var posicaoDaRota = endereco.indexOf('#') + 1;

		return endereco.substring(posicaoDaRota);
	};

	roteador.atualizar = function() {
		var rotaAntiCache = roteador.paginaAtual() + '?' + new Date().getTime();
		router.setRoute(rotaAntiCache);
	};

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
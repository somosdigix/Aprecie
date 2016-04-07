define([
	'director',
	'app/servicos/servicoDeAutenticacao'
], function(Router, servicoDeAutenticacao) {
	'use strict';

	var router;
	var roteador = {};
	var _controllerAtivo;

	roteador.configurar = function() {
		var rotas = {
			'/login': [middlewareDeAutenticacao, middlewareDeTransicaoDeTela, middlewareDeToolbar, limparTela, login],
			'/paginaInicial': [middlewareDeAutenticacao, middlewareDeTransicaoDeTela, middlewareDeToolbar, limparTela, paginaInicial],
			'/perfil/:colaboradorId': [middlewareDeAutenticacao, middlewareDeTransicaoDeTela, middlewareDeToolbar, limparTela, perfil],
			'/reconhecimentos/:colaboradorId/:valorId': [middlewareDeAutenticacao, middlewareDeTransicaoDeTela, middlewareDeToolbar, limparTela, reconhecimentos]
		};

		function limparTela() {
			$('#conteudo').empty();
		}

		function login() {
			require(['app/login/controller'], function(loginController) {
				_controllerAtivo = loginController;
				loginController.exibir();
			});
		}

		function paginaInicial() {
			require(['app/paginaInicial/controller'], function(paginaInicialController) {
				_controllerAtivo = paginaInicialController;
				paginaInicialController.exibir();
			});
		}

		function perfil(colaboradorId) {
			require(['app/perfil/controller'], function(perfilController) {
				_controllerAtivo = perfilController;
				perfilController.exibir(parseInt(colaboradorId));
			});
		}

		function reconhecimentos(colaboradorId, valorId) {
			require(['app/reconhecimentos/controller'], function(reconhecimentosController) {
				_controllerAtivo = reconhecimentosController;
				reconhecimentosController.exibir(parseInt(colaboradorId), parseInt(valorId));
			});
		}

		router = Router(rotas);
		router.init();
	};

	roteador.navegarPara = function(endereco) {
		window.location = '#' + endereco;
	};

	roteador.paginaAtual = function() {
		var endereco = window.location.toString();
		var posicaoDaRota = endereco.indexOf('#') + 1;

		if (posicaoDaRota === 0)
			return '';

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

	function middlewareDeTransicaoDeTela() {
		if (_controllerAtivo)
			_controllerAtivo.finalizar();
	}

	function middlewareDeToolbar() {
		require(['app/toolbar/toolbar'], function(toolbar) {
			if (servicoDeAutenticacao.jaEstaAutenticado() && roteador.paginaAtual() !== '/login') {
				toolbar.exibir();
				$('body').removeClass('body-login').addClass('body-app');
			}
			else {
				toolbar.esconder();
				$('body').removeClass('body-app').addClass('body-login');
			}
		});
	}

	return roteador;
});
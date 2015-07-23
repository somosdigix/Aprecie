define([
	'director'
], function(Router) {
	'use strict';

	var rotas = {};

	rotas.configurar = function() {
		var routes = {
			'/login': login,
			'/outraPagina': [middlewareDeAutenticacao, outraPagina]
		};

		function login() {
			console.log('login');
		}

		function scratch() {
			console.log('scratch');
		}

		function outraPagina() {
			console.log('outraPagina');
		}

		var router = Router(routes);
		router.init();
	};

	function middlewareDeAutenticacao() {
		var estaAutenticado = false;

		if (!estaAutenticado) {
			window.location = '/#/login';
			return false;
		}

		return true;
	}

	return rotas;
});
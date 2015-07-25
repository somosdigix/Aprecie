define(function() {
	'use strict';

	var cookieHelper = {};
	var prefixo = '@aprecie.me';

	cookieHelper.criar = function(chave, valor) {
		document.cookie = chave + prefixo + '=' + valor;
	};

	cookieHelper.obter = function(chave) {
		var cookies = obterCookies();
		var cookieEncontrado = cookies.filter(function(cookie) {
			return cookie.chave === chave + prefixo;
		})[0];

		console.log(cookies);
		console.log(cookieEncontrado);

		return cookieEncontrado.valor;
	};

	cookieHelper.remover = function(chave) {
		remover(chave + prefixo);
	};

	cookieHelper.limpar = function() {
		var cookies = obterCookies();

		cookies.map(function(cookie) {
			remover(cookie.chave);
		});
	};

	function remover(chave) {
		document.cookie = chave + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT';
	}

	function obterCookies() {
		var cookies = document.cookie.split('; ');

		return cookies.filter(function(cookie) {
			return cookie.indexOf(prefixo) > -1;
		}).map(function(cookie) {
			return new Cookie(cookie);
		});
	}

	function Cookie(cookie) {
		var valores = cookie.split('=');

		this.chave = valores[0];
		this.valor = valores[1];
	}

	return cookieHelper;
})
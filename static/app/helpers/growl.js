define([
	'jquery'
], function() {
	'use strict';
	
	var growl = {};
	var timer;

	growl.deSucesso = function() {
		$('div[data-js="growl"]').addClass('fundo-verde').removeClass('fundo-vermelho');
		return growl;
	}

	growl.deErro = function() {
		$('div[data-js="growl"]').addClass('fundo-vermelho').removeClass('fundo-verde');
		return growl;
	}

	growl.exibir = function(mensagem) {
		$('div[data-js="growl"] span').text(mensagem);
		$('div[data-js="growl"]').show();

		reiniciarTimer();
	};

	growl.esconder = function() {
		$('div[data-js="growl"]').hide();
	};

	function reiniciarTimer() {
		clearTimeout(timer);

		timer = setTimeout(growl.esconder, 3000);
	}

	return growl;
});
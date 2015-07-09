define([
	'jquery'
], function() {
	'use strict';
	
	var growl = {};

	growl.exibir = function(mensagem) {
		$('div[data-js="growl"] span').text(mensagem);
		$('div[data-js="growl"]').show();
	};

	growl.esconder = function() {
		$('div[data-js="growl"]').hide();
	};

	return growl;
});
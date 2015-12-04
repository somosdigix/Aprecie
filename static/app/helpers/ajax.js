define([
	'jquery'
], function($) {
	'use strict';

	var self = {};

	self.getJSON = function(url, parametros) {
		var acao = function(resolver, rejeitar) {
			$.getJSON(url, parametros).done(resolver).fail(rejeitar);
		};

		return new Promise(acao);
	};

	self.post = function(url, dados) {
		var acao = function(resolver, rejeitar) {
			$.post(url, dados).done(resolver).fail(rejeitar);
		};

		return new Promise(acao);
	}

	return self;
});
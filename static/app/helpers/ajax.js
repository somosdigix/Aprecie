define([
	'jquery'
], function($) {
	'use strict';

	var self = {};

	self.post = function(url, dados) {
		var acao = function(resolver, rejeitar) {
			$.post(url, dados).done(resolver).fail(rejeitar);
		};

		return new Promise(acao);
	}

	return self;
});
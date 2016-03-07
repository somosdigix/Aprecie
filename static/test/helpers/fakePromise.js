define(function() {
	'use strict';

	function FakePromise(dadosParaResolver, dadosParaRejeitar) {
		this.then = function(resolver) {
			resolver(dadosParaResolver);
		};

		this.catch = function(rejeitar) {
			rejeitar(dadosParaRejeitar);
		};
	}

	return FakePromise;
});
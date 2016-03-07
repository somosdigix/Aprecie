define([
	'jquery',
	'sandbox',
	'app/paginaInicial/valores'
], function($, Sandbox, valores) {
	'use strict';

	describe('Valores na página inicial', function() {
		var _sandbox;

		beforeEach(function() {
			_sandbox = new Sandbox();

			$('body').append('<main id="conteudo"></main>');
		});

		afterEach(function() {
			valores.finalizar();
		});

		it('deve exibir seu conteúdo', function() {
			valores.inicializar(_sandbox);

			expect($('li').length).toBe(7);
		});

		it('deve limpar o conteúdo ao finalizar', function() {
			valores.inicializar(_sandbox);

			valores.finalizar();

			expect($('#conteudo').html()).toBe('');
		});
	});
});
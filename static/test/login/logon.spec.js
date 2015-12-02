define([
	'jquery',
	'configuracoes',
	'sandbox',
	'app/login/logon',
	'jquery.inputmask'
], function($, configuracoes, Sandbox, logon) {
	'use strict';

	describe('Logon', function() {
		var _sandbox;

		beforeEach(function() {
			_sandbox = new Sandbox();
			$('body').addClass('body-app').append('<main id="conteudo"></main>');
		});

		afterEach(function() {
			$('#conteudo').remove();
		});

		it('deve exibir seu conteudo', function() {
			logon.inicializar(_sandbox);

			expect($('#cpf').length).toBe(1);
			expect($('#dataDeNascimento').length).toBe(1);
		});

		it('deve trocar a imagem de fundo', function() {
			logon.inicializar(_sandbox);

			expect($('body').attr('class')).toBe('body-login');
		});

		it('deve mascarar o campo de CPF', function() {
			logon.inicializar(_sandbox);

			$('#cpf').val('00000000000');

			expect($('#cpf').val()).toBe('000.000.000-00');
		});

		xit('deve focar campo de CPF', function() {
			logon.inicializar(_sandbox);
			
			expect($('#cpf').is(':focus')).toBe(true);
		});

		it('deve mascarar o campo de data de nascimento', function() {
			logon.inicializar(_sandbox);

			$('#dataDeNascimento').val('10102010');

			expect($('#dataDeNascimento').val()).toBe('10/10/2010');
		});

		xit('deve focar o campo de data de nascimento ao finalizar o preenchimento do CPF', function() {
			logon.inicializar(_sandbox);

			$('#cpf').val('00000000000').trigger('keyup');

			expect($('#dataDeNascimento').is(':focus')).toBe(true);
		});

		it('deve preencher os dados de login com dados falsos caso esteja em modo debug', function() {
			configuracoes.configurarDebug(true);

			logon.inicializar(_sandbox);

			expect($('#cpf').val()).toBe('000.000.000-00');
			expect($('#dataDeNascimento').val()).toBe('01/01/2015');
		});

		it('deve disparar evento de autenticação ao clicar para realizar login', function() {
			spyOn(_sandbox, 'notificar');
			logon.inicializar(_sandbox);

			$('button[data-js="autenticar"]').click();

			expect(_sandbox.notificar).toHaveBeenCalledWith('autenticar', '00000000000', '01/01/2015');
		});
	});
});
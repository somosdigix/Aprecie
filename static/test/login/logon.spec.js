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
			configuracoes.configurarDebug(false);
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

		it('deve focar campo de CPF', function() {
			logon.inicializar(_sandbox);

			expect(document.activeElement.id).toBe('cpf');
		});

		it('deve mascarar o campo de data de nascimento', function() {
			logon.inicializar(_sandbox);

			$('#dataDeNascimento').val('10102010');

			expect($('#dataDeNascimento').val()).toBe('10/10/2010');
		});

		it('deve focar o campo de data de nascimento ao finalizar o preenchimento do CPF', function() {
			logon.inicializar(_sandbox);

			$('#cpf').val('00000000000').trigger('keyup');

			expect(document.activeElement.id).toBe('dataDeNascimento');
		});

		it('deve preencher os dados de login com dados falsos caso esteja em modo debug', function() {
			configuracoes.configurarDebug(true);

			logon.inicializar(_sandbox);

			expect($('#cpf').val()).toBe('000.000.000-00');
			expect($('#dataDeNascimento').val()).toBe('01/01/2015');
		});

		it('deve vir com os dados de login vazios caso não esteja em modo debug', function() {
			configuracoes.configurarDebug(false);

			logon.inicializar(_sandbox);

			expect($('#cpf').val()).toBe('');
			expect($('#dataDeNascimento').val()).toBe('');
		});

		it('deve disparar evento de autenticação ao clicar para realizar login', function() {
			spyOn(_sandbox, 'notificar');
			logon.inicializar(_sandbox);
			$('#cpf').val('00000000000');
			$('#dataDeNascimento').val('01012015');

			$('button[data-js="autenticar"]').click();

			expect(_sandbox.notificar).toHaveBeenCalledWith('autenticar', '00000000000', '01/01/2015');
		});
	});
});
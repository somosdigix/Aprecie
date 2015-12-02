define([
	'gerenciadorDeModulos',
	'sandbox',
	'app/login/autenticacao'
], function(gerenciadorDeModulos, Sandbox, autenticacao) {
	'use strict';

	describe('Autenticacao', function() {
		var _sandbox, _dadosDeLogin;

		beforeEach(function() {
			_sandbox = new Sandbox(gerenciadorDeModulos);
			_dadosDeLogin = {
				cpf: '14114168133',
				data_de_nascimento: '01/08/1989'
			};

			spyOn(_sandbox, 'post').and.callFake(function() {
			}).and.returnValue({
				then: function() {}
			});
		});

		it('deve responder ao evento de autenticação', function() {
			autenticacao.inicializar(_sandbox);

			_sandbox.notificar('autenticar', _dadosDeLogin.cpf, _dadosDeLogin.data_de_nascimento);

			expect(_sandbox.post).toHaveBeenCalledWith('/login/entrar/', _dadosDeLogin);
		});

		xit('deve remover escuta do evento de autenticação ao finalizar', function() {

		});

		it('não deve autenticar com CPF vazio', function() {
			expect(function() {
				_sandbox.notificar('autenticar', '');
			}).toThrowError(ViolacaoDeRegra, 'CPF deve ser informado');
		});

		it('não deve autenticar sem CPF', function() {
			expect(function() {
				_sandbox.notificar('autenticar');
			}).toThrowError(ViolacaoDeRegra, 'CPF deve ser informado');
		});

		it('não deve autenticar com data de nascimento vazia', function() {
			expect(function() {
				_sandbox.notificar('autenticar', _dadosDeLogin.cpf, '');
			}).toThrowError(ViolacaoDeRegra, 'Data de nascimento deve ser informada');
		});

		it('não deve autenticar sem data de nascimento', function() {
			expect(function() {
				_sandbox.notificar('autenticar', _dadosDeLogin.cpf);
			}).toThrowError(ViolacaoDeRegra, 'Data de nascimento deve ser informada');
		});

		xit('deve preencher a sessão com dados do usuario autenticado', function() {
			autenticacao.inicializar(_sandbox);

			_sandbox.notificar('autenticar', _dadosDeLogin.cpf, _dadosDeLogin.data_de_nascimento);

			expect(_sandbox.post).toHaveBeenCalledWith('/login/entrar/', _dadosDeLogin);
		});

		xit('deve preencher o cookie com dados do usuario autenticado', function() {

		});

		xit('deve navegar para a página inicial ao terminar a autenticação', function() {

		});
	});
});
define([
	'fakePromise',
	'gerenciadorDeModulos',
	'sandbox',
	'app/login/autenticacao'
], function(FakePromise, gerenciadorDeModulos, Sandbox, autenticacao) {
	'use strict';

	describe('Autenticacao', function() {
		var _sandbox, _dadosDeLogin;

		beforeEach(function() {
			_sandbox = new Sandbox(gerenciadorDeModulos);
			_dadosDeLogin = {
				cpf: '14114168133',
				data_de_nascimento: '01/08/1989'
			};

			spyOn(_sandbox, 'post').and.returnValue(new FakePromise(_dadosDeLogin));
			spyOn(_sandbox, "preencherSessao");
			spyOn(_sandbox, "preencherCookie");
			spyOn(_sandbox, 'navegarPara');
		});

		afterEach(function() {
			autenticacao.finalizar(_sandbox);
		});

		it('deve responder ao evento de autenticação', function() {
			autenticacao.inicializar(_sandbox);

			_sandbox.notificar('autenticar', _dadosDeLogin.cpf, _dadosDeLogin.data_de_nascimento);

			expect(_sandbox.post).toHaveBeenCalledWith('/login/entrar/', _dadosDeLogin);
		});

		it('deve remover escuta do evento de autenticação ao finalizar', function() {
			autenticacao.finalizar();

			_sandbox.notificar('autenticar', _dadosDeLogin.cpf, _dadosDeLogin.data_de_nascimento);

			expect(_sandbox.post).not.toHaveBeenCalled();
		});

		it('não deve autenticar com CPF vazio', function() {
			autenticacao.inicializar(_sandbox);

			expect(function() {
				_sandbox.notificar('autenticar', '');
			}).toThrowError(ViolacaoDeRegra, 'CPF deve ser informado');
		});

		it('não deve autenticar sem CPF', function() {
			autenticacao.inicializar(_sandbox);

			expect(function() {
				_sandbox.notificar('autenticar');
			}).toThrowError(ViolacaoDeRegra, 'CPF deve ser informado');
		});

		it('não deve autenticar com data de nascimento vazia', function() {
			autenticacao.inicializar(_sandbox);

			expect(function() {
				_sandbox.notificar('autenticar', _dadosDeLogin.cpf, '');
			}).toThrowError(ViolacaoDeRegra, 'Data de nascimento deve ser informada');
		});

		it('não deve autenticar sem data de nascimento', function() {
			autenticacao.inicializar(_sandbox);

			expect(function() {
				_sandbox.notificar('autenticar', _dadosDeLogin.cpf);
			}).toThrowError(ViolacaoDeRegra, 'Data de nascimento deve ser informada');
		});

		it('deve preencher a sessão com dados do usuario autenticado', function() {
			autenticacao.inicializar(_sandbox);

			_sandbox.notificar('autenticar', _dadosDeLogin.cpf, _dadosDeLogin.data_de_nascimento);

			expect(_sandbox.preencherSessao).toHaveBeenCalledWith(_dadosDeLogin);
		});

		it('deve preencher o cookie com dados do usuario autenticado', function() {
			autenticacao.inicializar(_sandbox);

			_sandbox.notificar('autenticar', _dadosDeLogin.cpf, _dadosDeLogin.data_de_nascimento);

			expect(_sandbox.preencherCookie).toHaveBeenCalledWith(_dadosDeLogin);
		});

		it('deve navegar para a página inicial ao terminar a autenticação', function() {
			autenticacao.inicializar(_sandbox);

			_sandbox.notificar('autenticar', _dadosDeLogin.cpf, _dadosDeLogin.data_de_nascimento);

			expect(_sandbox.navegarPara).toHaveBeenCalledWith('/paginaInicial');
		});
	});
});
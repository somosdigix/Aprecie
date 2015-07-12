define([
	'app/helpers/cookie'
], function(cookie) {
	'use strict';

	describe('Cookie', function() {
		var cookieFalso = 'nome@outro.site=Renan';

		afterEach(function() {
			cookie.limpar();
			document.cookie = 'nome@outro.site=; expires=Thu, 01 Jan 1970 00:00:00 GMT';
		});

		it('deve quebrar o travis!', function() {
			expect(true).toBe(false);
		});

		it('deve criar um cookie contendo o prefixo da aplicação', function() {
			cookie.criar('teste', 1);

			var cookies = document.cookie;
			expect(cookies.indexOf('teste@aprecie.me=1') > -1).toBe(true);
		});

		it('deve obter o valor de um cookie', function() {
			cookie.criar('nome', 'Renan');

			var valor = cookie.obter('nome');

			expect(valor).toBe('Renan');
		});

		it('deve remover um determinado cookie', function() {
			document.cookie = 'nome@aprecie.me=Renan';
			document.cookie = 'sobrenome@aprecie.me=Siravegna';

			cookie.remover('nome');

			expect(document.cookie).toBe('sobrenome@aprecie.me=Siravegna');
		});

		it('deve limpar todos os cookies da aplicação, ignorando os demais', function() {
			document.cookie = 'nome@aprecie.me=Renan';
			document.cookie = cookieFalso;

			cookie.limpar();

			expect(document.cookie).toBe('nome@outro.site=Renan');
		});
	});
});
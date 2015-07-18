define([
	'jquery',
	'app/helpers/template'
], function($, template) {
	'use strict';

	describe('Visualizador de template', function() {

		beforeEach(function() {
			$('body').append('<div id="conteudo">aaa</div>');
		});

		afterEach(function() {
			$('#conteudo').remove();
		});

		it('deve limpar', function() {
			// act
			template.inserir('');

			// assert
			var conteudo = $('#conteudo').html();
			expect(conteudo).toBe('');
		});

		it('deve construir', function() {
			var novoConteudo = 'a';

			// act
			template.inserir(novoConteudo);

			// assert
			var conteudo = $('#conteudo').html();
			expect(conteudo).toBe(novoConteudo);
		});

		it('deve exibir modelo', function() {
			var novoConteudo = '<span class="nome">{{this.nome}}</span>' +
				'<span class="sobrenome">{{this.sobrenome}}</span>';
			var modelo = {
				nome: 'Renan',
				sobrenome: 'Siravegna'
			};

			template.inserir(novoConteudo, modelo);

			var conteudoDoNome = $('span.nome').html();
			var conteudoDoSobrenome = $('span.sobrenome').html();
			expect(conteudoDoNome).toBe('Renan');
			expect(conteudoDoSobrenome).toBe('Siravegna');
		});

		it('deve exibir uma lista de modelos', function() {
			var novoConteudo = '{{#.}}<div class="pessoa">{{this.nome}}</div>{{/.}}'
			var pessoas = [{
				nome: 'Renan'
			}, {
				nome: 'Renan'
			}];

			template.inserir(novoConteudo, pessoas);

			var quantidadeDePessoas = $('div.pessoa').length;
			expect(quantidadeDePessoas).toBe(2);
		});
	});
});
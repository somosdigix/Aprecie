define([
	'jquery',
	'app/helpers/template'
], function($, template) {
	'use strict';

	describe('Visualizador de template', function() {

		beforeEach(function() {
			$('body')
				.append('<div id="conteudo"><span>Conteúdo qualquer</span></div>')
				.append('<div id="outroConteudo"><span>Conteúdo qualquer 2</span></div>');
		});

		afterEach(function() {
			$('#conteudo, #outroConteudo').remove();
		});

		it('deve limpar', function() {
			template.exibir('');

			var conteudo = $('#conteudo').html();
			expect(conteudo).toBe('');
		});

		it('deve construir', function() {
			var novoConteudo = '<div>Novo conteúdo</div>';

			template.exibir(novoConteudo);

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

			template.exibir(novoConteudo, modelo);

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

			template.exibir(novoConteudo, pessoas);

			var quantidadeDePessoas = $('div.pessoa').length;
			expect(quantidadeDePessoas).toBe(2);
		});

		it('deve exibir em um container específico', function() {
			var novoConteudo = '<span>Teste</span>';

			template.exibirEm('#outroConteudo', novoConteudo);

			var conteudoDoContainer = $('#outroConteudo').html();
			expect(conteudoDoContainer).toBe(novoConteudo);
		});

		it('deve acrescentar um conteudo em um container específico', function() {
			var conteudo = '<span>Teste</span>';
			var conteudoEsperado = conteudo + conteudo;
			template.exibirEm('#outroConteudo', conteudo);

			template.acrescentarEm('#outroConteudo', conteudo);

			var conteudoDoContainer = $('#outroConteudo').html();
			expect(conteudoDoContainer).toBe(conteudoEsperado);
		});
	});
});
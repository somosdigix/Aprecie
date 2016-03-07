define([
	'jquery',
	'fakePromise',
	'sandbox',
	'app/paginaInicial/apreciacoes',
	'handlebars'
], function($, FakePromise, Sandbox, apreciacoes, Handlebars) {
	'use strict';

	describe('Listagem de apreciações na página inicial', function() {
		var _sandbox, _ultimosReconhecimentos;

		beforeEach(function() {
			_sandbox = new Sandbox();
			_ultimosReconhecimentos = [{
				data: '10 de Novembro de 2015 - 13:24',
				id_do_reconhecedor: 1,
				nome_do_reconhecedor: 'José',
				id_do_reconhecido: 2,
				nome_do_reconhecido: 'Maria',
				valor: 'Alegria',
				justificativa: 'Você é muito feliz.'
			}];

			spyOn(_sandbox, 'getJSON').and.returnValue(new FakePromise(_ultimosReconhecimentos));
			spyOn(_sandbox, 'navegarPara');
			$('body').append('<main id="conteudo"></main>');

			// TODO: Tirar este test double daqui
			Handlebars.registerHelper('foto', function() {
				return '';
			});
		});

		afterEach(function() {
			apreciacoes.finalizar();
		});

		it('deve exibir seu conteúdo', function() {
			apreciacoes.inicializar(_sandbox);

			expect($('div.feed-principal').length).toBe(1);
		});

		it('não deve limpar o conteúdo anterior ao exibir', function() {
			$('#conteudo').append('<span class="dummy"></span>');

			apreciacoes.inicializar(_sandbox);

			expect($('#conteudo span.dummy').length).toBe(1);
		});

		it('deve limpar o conteúdo ao finalizar', function() {
			apreciacoes.inicializar(_sandbox);

			apreciacoes.finalizar();

			expect($('#conteudo').html()).toBe('');
		});

		it('deve limpar o evento de visualizar o perfil da pessoa ao finalizar', function() {
			apreciacoes.inicializar(_sandbox);

			apreciacoes.finalizar();
			$('section.caixa-feed strong.nome').click();

			expect(_sandbox.navegarPara).not.toHaveBeenCalled();
		});

		it('deve exibir a data do último reconhecimento realizado', function() {
			apreciacoes.inicializar(_sandbox);
			var reconhecimento = $('section.caixa-feed');

			expect(reconhecimento.find('div.data').text()).toBe('10 de Novembro de 2015 - 13:24');
		});

		it('deve exibir o nome do reconhecedor do último reconhecimento realizado', function() {
			apreciacoes.inicializar(_sandbox);
			var reconhecimento = $('section.caixa-feed');

			expect(reconhecimento.find('strong.apreciador').text()).toBe('José');
		});

		it('deve exibir o nome do reconhecido do último reconhecimento realizado', function() {
			apreciacoes.inicializar(_sandbox);
			var reconhecimento = $('section.caixa-feed');

			expect(reconhecimento.find('strong.nome').text()).toBe('Maria');
		});

		it('deve exibir o valor do último reconhecimento realizado', function() {
			apreciacoes.inicializar(_sandbox);
			var reconhecimento = $('section.caixa-feed');

			expect(reconhecimento.find('div.valor').html()).toBe('Alegria');
		});

		it('deve exibir a justificativa do último reconhecimento realizado', function() {
			apreciacoes.inicializar(_sandbox);
			var reconhecimento = $('section.caixa-feed');

			expect(reconhecimento.find('div.informacoes p').text().trim()).toBe('Você é muito feliz.');
		});

		it('deve exibir uma caixa para cada reconhecimento realizado', function() {
			var reconhecimentosDummy = [{}, {}, {}, {}, {}];
			_sandbox.getJSON.and.returnValue(new FakePromise(reconhecimentosDummy));

			apreciacoes.inicializar(_sandbox);

			expect($('section.caixa-feed').length).toBe(5);
		});

		it('deve requisitar todos os últimos reconhecimentos realizados para exibi-los', function() {
			apreciacoes.inicializar(_sandbox);

			expect(_sandbox.getJSON).toHaveBeenCalledWith('/reconhecimentos/ultimos/');
		});

		it('deve permitir ir ao perfil do reconhecedor', function() {
			apreciacoes.inicializar(_sandbox);

			$('section.caixa-feed strong.apreciador').click();

			expect(_sandbox.navegarPara).toHaveBeenCalledWith('/perfil/1');
		});

		it('deve permitir ir ao perfil do reconhecido', function() {
			apreciacoes.inicializar(_sandbox);

			$('section.caixa-feed strong.nome').click();

			expect(_sandbox.navegarPara).toHaveBeenCalledWith('/perfil/2');
		});
	});
});
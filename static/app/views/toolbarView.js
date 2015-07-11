define([
	'jquery',
	'handlebars',
	'text!partials/toolbarTemplate.html',
	'jquery-ui'
], function($, Handlebars, toolbarTemplate, sessaoDeUsuario) {
	'use strict';

	var toolbarView = {};

	toolbarView.exibir = function(callback) {
		$.getJSON('/login/obter_funcionarios', function(colaboradores) {
			var configuracoesDoAutocomplete = {
				source: converterParaAutocomplete(colaboradores),
				minLength: 3,
				select: selecionar
			};

			$('section[data-js="toolbar"]')
				.show()
				.html(toolbarTemplate)
				.on('click', 'div[data-js="retornar-para-pagina-inicial"]', retornarParaPaginaInicial)
				.on('click', 'div[data-js="sair"]', sair);
			$('#colaborador').off().autocomplete(configuracoesDoAutocomplete);

			if (callback)
				callback();
		});
	};

	toolbarView.esconder = function() {
		$('section[data-js="toolbar"]').hide(toolbarTemplate).empty();
	};

	function converterParaAutocomplete(colaboradores) {
		return colaboradores.map(function(colaborador) {
			colaborador.value = colaborador.id;
			colaborador.label = colaborador.nome;

			return colaborador;
		});
	}

	function selecionar(evento, ui) {
		require(['app/views/reconhecimentosView'], function(reconhecimentosView) {
			var colaborador = ui.item;
			$('#colaborador').val('').blur();
			reconhecimentosView.exibir(colaborador.id);
		});

		evento.preventDefault();
	}

	function retornarParaPaginaInicial() {
		require(['app/views/paginaInicialView'], function(paginaInicialView) {
			paginaInicialView.exibir();
		});
	}

	function sair() {
		require(['app/views/loginView'], function(loginView) {
			loginView.exibir();
		});
	}

	return toolbarView;
});
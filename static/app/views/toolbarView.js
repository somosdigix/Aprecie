define([
	'jquery',
	'handlebars',
	'text!partials/toolbarTemplate.html',
	'app/models/sessaoDeUsuario',
	'jquery-ui'
], function($, Handlebars, toolbarTemplate, sessaoDeUsuario) {
	'use strict';

	var toolbarView = {};

	toolbarView.exibir = function(callback) {
		var template = Handlebars.compile(toolbarTemplate);

		$.getJSON('/login/obter_funcionarios', function(colaboradores) {
			var configuracoesDoAutocomplete = {
				source: converterParaAutocomplete(colaboradores),
				minLength: 1,
				select: selecionar
			};

			$('section[data-js="toolbar"]')
				.show()
				.html(template(sessaoDeUsuario))
				.on('click', 'div[data-js="pagina-inicial"]', paginaInicial)
				.on('click', 'div[data-js="meu-perfil"]', meuPerfil)
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

	function paginaInicial() {
		require(['app/views/paginaInicialView'], function(paginaInicialView) {
			paginaInicialView.exibir();
		});
	}

	function meuPerfil() {
		require(['app/views/reconhecimentosView'], function(reconhecimentosView) {
			reconhecimentosView.exibir(sessaoDeUsuario.id);
		});
	}

	function sair() {
		require(['app/views/loginView'], function(loginView) {
			loginView.exibir();
		});
	}

	return toolbarView;
});
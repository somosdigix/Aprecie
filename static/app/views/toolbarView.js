define([
	'jquery',
	'template',
	'text!partials/toolbarTemplate.html',
	'sessaoDeUsuario',
	'jquery-ui'
], function($, template, toolbarTemplate, sessaoDeUsuario) {
	'use strict';

	var toolbarView = {};

	toolbarView.exibir = function(callback) {
		$.getJSON('/login/obter_funcionarios', function(data) {
			template.exibirEm('header[data-js="toolbar"]', toolbarTemplate, sessaoDeUsuario);

			var configuracoesDoAutocomplete = {
				source: converterParaAutocomplete(data.colaboradores),
				minLength: 1,
				select: selecionar
			};

			$('header[data-js="toolbar"]')
				.show()
				.on('click', 'div[data-js="pagina-inicial"]', paginaInicial)
				.on('click', 'div[data-js="meu-perfil"]', meuPerfil)
				.on('click', 'div[data-js="sair"]', sair);
			$('#colaborador').off().autocomplete(configuracoesDoAutocomplete);

			if (callback)
				callback();
		});
	};

	toolbarView.esconder = function() {
		$('header[data-js="toolbar"]').hide(toolbarTemplate).empty();
	};

	function converterParaAutocomplete(colaboradores) {
		return colaboradores.map(function(colaborador) {
			colaborador.value = colaborador.id;
			colaborador.label = colaborador.nome;

			return colaborador;
		});
	}

	function selecionar(evento, ui) {
		require(['app/views/perfilView'], function(perfilView) {
			var colaborador = ui.item;
			$('#colaborador').val('').blur();
			perfilView.exibir(colaborador.id);
		});

		evento.preventDefault();
	}

	function paginaInicial() {
		require(['app/views/paginaInicialView'], function(paginaInicialView) {
			paginaInicialView.exibir();
		});
	}

	function meuPerfil() {
		require(['app/views/perfilView'], function(perfilView) {
			perfilView.exibir(sessaoDeUsuario.id);
		});
	}

	function sair() {
		require([
			'cookie',
			'app/views/loginView'
		], function(cookie, loginView) {
			cookie.limpar();
			toolbarView.esconder();
			loginView.exibir();
		});
	}

	return toolbarView;
});
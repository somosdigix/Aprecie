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
		$.getJSON('/login/obter_colaboradores', function(data) {
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
				.on('click', 'div[data-js="tratar-menu-mobile"]', tratarMenuMobile)
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
			colaborador.id = colaborador.id;
			colaborador.label = colaborador.nome;
			colaborador.value = colaborador.nome;

			return colaborador;
		});
	}

	function selecionar(evento, ui) {
		require(['roteador'], function(roteador) {
			var colaborador = ui.item;
			$('#colaborador').val('').blur();

			roteador.navegarPara('/perfil/' + colaborador.id);
		});

		evento.preventDefault();
	}

	function paginaInicial() {
		require(['roteador'], function(roteador) {
			roteador.navegarPara('/paginaInicial');
		});
	}

	function meuPerfil() {
		require(['roteador'], function(roteador) {
			roteador.navegarPara('/perfil/' + sessaoDeUsuario.id);
		});
	}

	function tratarMenuMobile() {
		$('div[data-js="menu-mobile"]').toggleClass('aberto');
	}

	function sair() {
		require([
			'app/helpers/cookie',
			'roteador'
		], function(cookie, roteador) {
			cookie.limpar();
			toolbarView.esconder();
			roteador.navegarPara('/login');
		});
	}

	return toolbarView;
});
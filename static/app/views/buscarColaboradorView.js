define([
	'jquery',
	'handlebars',
	'text!partials/buscarColaboradorTemplate.html',
	'jquery-ui'
], function($, Handlebars, buscarColaboradorTemplate, sessaoDeUsuario) {
	'use strict';

	var buscarColaboradorView = {};

	buscarColaboradorView.exibir = function(callback) {
		$.getJSON('/login/obter_funcionarios', function(colaboradores) {
			var configuracoesDoAutocomplete = {
				source: converterParaAutocomplete(colaboradores),
				minLength: 3,
				select: selecionar
			};

			$('section[data-js="toolbar"]').show().html(buscarColaboradorTemplate);
			$('#colaborador').off().autocomplete(configuracoesDoAutocomplete);

			if (callback)
				callback();
		});
	};

	buscarColaboradorView.esconder = function() {
		$('section[data-js="toolbar"]').hide(buscarColaboradorTemplate).empty();
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

	return buscarColaboradorView;
});
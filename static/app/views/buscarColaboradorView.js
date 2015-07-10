define([
	'jquery',
	'handlebars',
	'text!partials/buscarColaboradorTemplate.html',
	'jquery-ui'
], function($, Handlebars, buscarColaboradorTemplate, sessaoDeUsuario) {
	'use strict';

	var buscarColaboradorView = {};

	buscarColaboradorView.exibir = function() {
		document.querySelector('#conteudo').innerHTML = buscarColaboradorTemplate;

		$.getJSON('/login/obter_funcionarios', function(colaboradores) {
			var configuracoesDoAutocomplete = {
				source: converterParaAutocomplete(colaboradores),
				minLength: 3,
				select: selecionar
			};

			$('#colaborador').off().autocomplete(configuracoesDoAutocomplete);
		});

		$('#conteudo').off().on('click', 'a[data-js="voltar"]', voltar);
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
			reconhecimentosView.exibir(colaborador.id);
		});

		evento.preventDefault();
	}

	function voltar() {
		require(['app/views/paginaInicialView'], function(paginaInicialView) {
			paginaInicialView.exibir();
		});
	}

	return buscarColaboradorView;
});
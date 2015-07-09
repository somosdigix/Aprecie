define([
	'jquery',
	'handlebars',
	'text!partials/buscarColaboradorTemplate.html',
	'jquery-ui'
], function($, Handlebars, buscarColaboradorTemplate, sessaoDeUsuario) {
	'use strict';

	var buscarColaboradorView = {};

	var configuracoesDoAutocomplete = {
		source: '/login/obter_funcionarios/',
		minLength: 1,
		select: selecionar
	};

	buscarColaboradorView.exibir = function() {
		document.querySelector('#conteudo').innerHTML = buscarColaboradorTemplate;

		$('#colaborador')
			.off()
			.autocomplete(configuracoesDoAutocomplete)
			.autocomplete('instance')._renderItem = exibirItem;
	};

	function exibirItem(lista, item) {
		return $('<li>')
			.append('<a data-colaborador-id="' + item.id + '">' + item.nome + '</a>' )
			.appendTo(lista);
	}

	function selecionar(evento, ui) {
		require(['app/views/reconhecimentosView'], function(reconhecimentosView) {
			var colaborador = ui.item;
			reconhecimentosView.exibir(colaborador.id);
		});

		evento.preventDefault();
	}

	return buscarColaboradorView;
});
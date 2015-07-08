define([
	'jquery',
	'handlebars',
	'text!partials/buscarColaboradorTemplate.html',
	'jquery-ui'
], function($, Handlebars, buscarColaboradorTemplate) {
	'use strict';

	var buscarColaboradorView = {};

	var configuracoesDoAutocomplete = {
		source: '/login/obter_funcionarios/',
		minLength: 3,
		select: selecionar
	};

	buscarColaboradorView.exibir = function() {
		document.querySelector('#conteudo').innerHTML = buscarColaboradorTemplate;

		$('#elogiado')
			.off()
			.autocomplete(configuracoesDoAutocomplete)
			.autocomplete('instance')._renderItem = exibirItem;
	};

	function exibirItem(lista, item) {
		return $('<li>')
			.append('<a data-cpf="' + item.cpf + '">' + item.nome + '</a>' )
			.appendTo(lista);
	}

	function selecionar(evento, ui) {
		require(['app/views/reconhecimentosView'], function(reconhecimentosView) {
			var funcionario = ui.item;
			reconhecimentosView.exibir(funcionario.cpf);
		});

		evento.preventDefault();
	}

	return buscarColaboradorView;
});
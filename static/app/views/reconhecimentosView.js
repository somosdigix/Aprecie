define([
	'jquery',
	'handlebars',
	'text!partials/reconhecimentosTemplate.html'
], function($, Handlebars, reconhecimentosTemplate) {
	'use strict';

	var reconhecimentosView = {};

	reconhecimentosView.exibir = function(colaboradorId) {
		var data = {
			id_do_reconhecido: colaboradorId
		};

		$.getJSON('/reconhecimentos/funcionario/', data, function(reconhecimentosDoColaborador) {
			var template = Handlebars.compile(reconhecimentosTemplate);
			$('#conteudo').empty().html(template(reconhecimentosDoColaborador));
		});

		$('#conteudo').off()
			.on('click', 'span[data-js="abrirJustificativa"]', abrirJustificativa)
			.on('click', 'button[data-js="reconhecer"]', reconhecer)
			.on('click', 'button[data-js="fecharJustificativa"]', fecharJustificativa)
			.on('click', 'a[data-js="voltar"]', voltar);
	};

	function abrirJustificativa() {
		var valorId = $(this).data('valor-id');

		$('#valorId').val(valorId);

		$('div[data-js="justificativa"]').dialog({
			title: 'Justificativa',
			width: 320,
			autoOpen: true,
			appendTo: '#conteudo',
			modal: true
		});
	}

	function reconhecer() {
		require(['app/models/reconhecerViewModel'], function(ReconhecerViewModel) {
			var reconhecerViewModel = new ReconhecerViewModel();

			$.post('/reconhecimentos/reconhecer/', reconhecerViewModel, function() {
				fecharJustificativa();
				reconhecimentosView.exibir(reconhecerViewModel.id_do_reconhecido);
			});
		});
	}

	function fecharJustificativa() {
		$('div[data-js="justificativa"]').dialog('close');
	}

	function voltar() {
		require(['app/views/buscarColaboradorView'], function(buscarColaboradorView) {
			buscarColaboradorView.exibir();
		});
	}

	return reconhecimentosView;
});
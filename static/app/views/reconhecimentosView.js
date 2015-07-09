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
			.on('click', '[data-js="reconhecer"]', reconhecer)
			.on('click', '[data-js="voltar"]', voltar);
	};

	function reconhecer() {
		var elemento = $(this);

		require([
			'app/models/sessaoDeUsuario',
			'app/models/reconhecerViewModel'
		], function(sessaoDeUsuario, ReconhecerViewModel) {
			var reconhecerViewModel = new ReconhecerViewModel(sessaoDeUsuario.id, elemento);

			$.post('/reconhecimentos/reconhecer/', reconhecerViewModel, function() {
				reconhecimentosView.exibir(elemento.data('colaborador-id'));
			});
		});
	}

	function voltar() {
		require(['app/views/buscarColaboradorView'], function(buscarColaboradorView) {
			buscarColaboradorView.exibir();
		});
	}

	return reconhecimentosView;
});
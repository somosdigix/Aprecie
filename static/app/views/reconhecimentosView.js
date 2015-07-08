define([
	'jquery',
	'handlebars',
	'text!partials/reconhecimentosTemplate.html'
], function($, Handlebars, reconhecimentosTemplate) {
	'use strict';

	var reconhecimentosView = {};

	reconhecimentosView.exibir = function(colaboradorId) {
		var data = {
			'colaboradorId': colaboradorId
		};

		$.post('/reconhecimentos/funcionario/', data, function(reconhecimentosDoColaborador) {
			var template = Handlebars.compile(reconhecimentosTemplate);
			$('#conteudo').empty().html(template(reconhecimentosDoColaborador));
		});

		$('#conteudo').off()
			.on('click', '[data-js="reconhecer"]', reconhecer)
			.on('click', '[data-js="voltar"]', voltar);
	};

	function reconhecer() {
		require(['app/models/sessaoDeUsuario'], function(sessaoDeUsuario) {
			var data = {
				id_do_reconhecedor: sessaoDeUsuario.id,
				id_do_reconhecido: $(this).data('colaborador-id'),
				id_do_valor: $(this).data('valor-id'),
				justificativa: 'Justificativa default'
			};

			$.post('/reconhecimentos/reconhecer/', data, function() {
				reconhecimentosView.exibir();
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
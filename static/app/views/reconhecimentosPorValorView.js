define([
	'jquery',
	'template',
	'text!partials/reconhecimentosTemplate.html',
	'sessaoDeUsuario',
	'app/views/iconesDosValoresHelpers'
], function($, template, reconhecimentosTemplate, sessaoDeUsuario) {
	'use strict';

	var reconhecimentosPorValorView = {};

	reconhecimentosPorValorView.exibir = function(colaboradorId, valorId) {
		$('#conteudo')
			.off()
			.on('click', 'button[data-js="voltar-ao-perfil"]', function() {
				voltarParaPerfil(colaboradorId);
			});

		$.getJSON('/reconhecimentos/' + colaboradorId + '/' + valorId, {}, function(resposta) {
			template.exibir(reconhecimentosTemplate, resposta);

			if (sessaoDeUsuario.id !== colaboradorId) {
				$('p[data-js="reconhecer"], button[data-js="reconhecer"]').show();
				$('#conteudo').on('click', 'button[data-js="reconhecer"]', reconhecer);
			}
		});
	};

	function reconhecer() {
		require([
			'app/models/reconhecerViewModel',
			'growl',
			'roteador'
		], function(ReconhecerViewModel, growl, roteador) {
			var reconhecerViewModel = new ReconhecerViewModel();
			validarOperacao(reconhecerViewModel);

			$.post('/reconhecimentos/reconhecer/', reconhecerViewModel, function() {
				growl.deSucesso().exibir('Reconhecimento realizado com sucesso');
				roteador.atualizar();
			});
		});
	}

	function validarOperacao(reconhecerViewModel) {
		if (reconhecerViewModel.justificativa === '')
			throw new ViolacaoDeRegra('Sua justificativa deve ser informada');
	}

	function voltarParaPerfil(reconhecidoId) {
		require(['roteador'], function(roteador) {
			roteador.navegarPara('/perfil/' + reconhecidoId);
		});
	}

	return reconhecimentosPorValorView;
});
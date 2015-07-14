define([
	'jquery',
	'handlebars',
	'text!partials/perfilTemplate.html',
	'text!partials/reconhecimentosPorReconhecedorTemplate.html',
	'sessaoDeUsuario',
	'app/views/iconesDosValoresHelpers'
], function($, Handlebars, perfilTemplate, reconhecimentosPorReconhecedorTemplate, sessaoDeUsuario) {
	'use strict';

	var perfilView = {};

	perfilView.exibir = function(colaboradorId) {
		var data = {
			id_do_reconhecido: colaboradorId
		};

		$.when(
			$.getJSON('/reconhecimentos/funcionario/', data),
			$.getJSON('/reconhecimentos/por_reconhecedor/', data)
		).then(function(resposta1, resposta2) {
			var reconhecimentosDoColaborador = resposta1[0];
			var reconhecimentosPorReconhecedor = resposta2[0];

			var template = Handlebars.compile(perfilTemplate);
			var dados = {
				reconhecimentosDoColaborador: reconhecimentosDoColaborador,
				reconhecimentosPorReconhecedor: reconhecimentosPorReconhecedor
			};

			$('#conteudo').empty().html(template(dados));
			exibirTeste(colaboradorId);

			$('#conteudo').off()
				.on('click', 'span[data-js="abrirJustificativa"]', abrirJustificativa)
				.on('click', 'button[data-js="reconhecer"]', reconhecer)
				.on('click', 'button[data-js="fecharJustificativa"]', fecharJustificativa);

			if (sessaoDeUsuario.id !== colaboradorId) {
				$('span[data-js="abrirJustificativa"]').show();
				$('#conteudo').on('click', 'button[data-js="fecharJustificativa"]', fecharJustificativa);
			}
		});
	};

	function exibirTeste(colaboradorId) {
		var data = {
			id_do_reconhecido: colaboradorId
		};

		var template = Handlebars.compile(reconhecimentosPorReconhecedorTemplate);

		$.getJSON('/reconhecimentos/por_reconhecedor/', data, function(reconhecimentosPorReconhecedor) {
			reconhecimentosPorReconhecedor.map(function(reconhecimento) {
				var secaoDoValor = $('section[data-valor-id="' + reconhecimento.id_do_valor + '"]');
				secaoDoValor.append(template(reconhecimento));
			});
		});
	}

	function abrirJustificativa() {
		var objetoClicado = this;

		require(['growl'], function(growl) {
			var valorId = $(objetoClicado).data('valor-id');

			$('#valorId').val(valorId);

			$('div[data-js="justificativa"]').dialog({
				title: 'Justificativa',
				width: 320,
				autoOpen: true,
				appendTo: '#conteudo',
				modal: true,
				close: function() {
					growl.esconder();
				}
			});
		});
	}

	function reconhecer() {
		require([
			'app/models/reconhecerViewModel',
			'growl'
		], function(ReconhecerViewModel, growl) {
			var reconhecerViewModel = new ReconhecerViewModel();
			validarOperacao(reconhecerViewModel);

			$.post('/reconhecimentos/reconhecer/', reconhecerViewModel, function() {
				fecharJustificativa();
				growl.deSucesso().exibir('Reconhecimento realizado com sucesso');
				perfilView.exibir(reconhecerViewModel.id_do_reconhecido);
			});
		});
	}

	function validarOperacao(reconhecerViewModel) {
		if (reconhecerViewModel.justificativa === '')
			throw new ViolacaoDeRegra('Sua justificativa deve ser informada');
	}

	function fecharJustificativa() {
		$('div[data-js="justificativa"]').dialog('close');
	}

	return perfilView;
});
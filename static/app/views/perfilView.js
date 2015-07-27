define([
	'jquery',
	'template',
	'text!partials/perfilTemplate.html',
	'app/views/reconhecimentosPorReconhecedorView',
	'sessaoDeUsuario',
	'app/views/iconesDosValoresHelpers'
], function($, template, perfilTemplate, reconhecimentosPorReconhecedorView, sessaoDeUsuario) {
	'use strict';

	var perfilView = {};

	perfilView.exibir = function(colaboradorId) {
		$.getJSON('/reconhecimentos/funcionario/' + colaboradorId, {}, function(reconhecimentosDoColaborador) {
			template.exibir(perfilTemplate, reconhecimentosDoColaborador);

			$('#conteudo').off()
				.on('click', 'button[data-js="reconhecer"]', reconhecer)
				.on('click', 'button[data-js="fecharJustificativa"]', fecharJustificativa);

			if (sessaoDeUsuario.id !== colaboradorId)
				$('#conteudo')
					.on('click', 'section[data-js="abrir-justificativa"]', abrirJustificativa)
					.on('click', 'button[data-js="fecharJustificativa"]', fecharJustificativa);
			else {
				$('span.ion-camera').show();
				$('#conteudo').on('click', 'div[data-js="foto"]', enviarFoto);
				$('input[data-js="alterar-foto"]').off().on('change', alterarFoto);
			}

			// reconhecimentosPorReconhecedorView.exibir(colaboradorId);
		});
	};

	function abrirJustificativa() {
		var objetoClicado = $(this);

		require(['growl'], function(growl) {
			var valorId = objetoClicado.data('valor-id');

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
			'growl',
			'roteador'
		], function(ReconhecerViewModel, growl, roteador) {
			var reconhecerViewModel = new ReconhecerViewModel();
			validarOperacao(reconhecerViewModel);

			$.post('/reconhecimentos/reconhecer/', reconhecerViewModel, function() {
				fecharJustificativa();
				growl.deSucesso().exibir('Reconhecimento realizado com sucesso');

				// TODO: Descobrir como atualiza a mesma página pelo roteador
				perfilView.exibir(reconhecerViewModel.id_do_reconhecido)
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

	function enviarFoto() {
		$('input[data-js="alterar-foto"]').trigger('click');
	}

	function alterarFoto() {
		var arquivo = this.files[0];

		if (arquivo.type.indexOf('image/') === -1)
			throw new ViolacaoDeRegra('Apenas imagens podem ser enviadas para seu perfil');

		var reader = new FileReader();

		reader.onload = function(progressEvent) {
			var data = {
				id_do_colaborador: sessaoDeUsuario.id,
				nova_foto: reader.result
			};

			$.post('/login/alterar_foto/', data, function() {
				$('img[data-js="foto"]').attr('src', reader.result);
				$('img[data-js="foto-miniatura"]').attr('src', reader.result);
			});
		};

		if (arquivo)
			reader.readAsDataURL(arquivo);
	}

	return perfilView;
});
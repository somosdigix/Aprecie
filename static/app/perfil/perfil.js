define([
	'jquery',
	'template',
	'text!app/perfil/perfilTemplate.html',
	'sessaoDeUsuario',
	'app/botaoReconhecer/botaoReconhecer'
], function ($, template, perfilTemplate, sessaoDeUsuario, botaoReconhecer) {
	'use strict';

	var _self = {};
	var _sandbox;

	_self.inicializar = function (sandbox, colaboradorId) {
		_sandbox = sandbox;

		$.getJSON('/reconhecimentos/colaborador/' + colaboradorId, function (reconhecimentosDoColaborador) {
			template.exibir(perfilTemplate, reconhecimentosDoColaborador);

			$('#conteudo')
				.on('click', 'div[data-js="exibir-reconhecimentos"]', exibirReconhecimentos);

			if (sessaoDeUsuario.id === colaboradorId) {
				$('span.ion-camera').show();
				$('#conteudo').on('click', 'div[data-js="foto"]', abrirSelecaoDeImagens);
				$('input[data-js="alterar-foto"]').off().on('change', alterarFoto);
				$('button[data-js="botao-apreciar"]').hide();
			}
			else {

				$('button[data-js="botao-apreciar"]').show().on('click', apreciar);
			}

			_sandbox.notificar('exibir-apreciacoes');
		});
	};

	_self.finalizar = function () {
		$('#conteudo').off();
	}

	function apreciar(){
		botaoReconhecer.exibirModal();

		var colaborador = {
			id_colaborador: parseInt($('#reconhecidoId').val()),
			nome: document.getElementById('reconhecidoNome').innerHTML,
		};
		
		botaoReconhecer.selecionarReconhecido(colaborador);
	}

	function exibirReconhecimentos() {
		var objetoClicado = $(this);

		require(['roteador'], function (roteador) {
			var pilarId = objetoClicado.data('pilar-id');
			var colaboradorId = $("#reconhecidoId").val();

			roteador.navegarPara('/reconhecimentos/' + colaboradorId + '/' + pilarId);
		});
	}

	// TODO: Modular esse envio de foto e aliar com webcomponent
	function abrirSelecaoDeImagens() {
		$('input[data-js="alterar-foto"]').trigger('click');
	}

	function alterarFoto() {
		var arquivo = this.files[0];

		if (arquivo.size > 2621440)
			throw new ViolacaoDeRegra('A sua foto pode ter no máximo 2,5 MB de tamanho');

		if (arquivo.type.indexOf('image/') === -1)
			throw new ViolacaoDeRegra('Apenas imagens podem ser enviadas para seu perfil');

		var reader = new FileReader();

		reader.onload = function (progressEvent) {
			var data = {
				id_do_colaborador: sessaoDeUsuario.id,
				nova_foto: reader.result
			};

			$.post('/login/alterar_foto/', data)
				.done(function () {
					$('img[data-js="foto"]').attr('src', reader.result);
					$('div[data-js="meu-perfil"] img').attr('src', reader.result);
				})
				.fail(function () {
					require(['growl'], function (growl) {
						growl.deErro().exibir('Não foi possível alterar sua foto :(');
					});
				});
		};

		if (arquivo)
			reader.readAsDataURL(arquivo);
	}

	return _self;
});

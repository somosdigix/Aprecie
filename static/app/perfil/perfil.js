define([
	'jquery',
	'template',
	'text!app/perfil/perfilTemplate.html',
	'sessaoDeUsuario',
	'app/botaoReconhecer/botaoReconhecer',
  'app/helpers/administradorHelper'
], function ($, template, perfilTemplate, sessaoDeUsuario, botaoReconhecer, administradorHelper) {
	'use strict';

	var _self = {};
	var _sandbox;

	_self.inicializar = function (sandbox, colaboradorId) {
		_sandbox = sandbox;

		$.getJSON(
			"/reconhecimentos/colaborador/" + colaboradorId,
			function (reconhecimentosDoColaborador) {
				template.exibir(perfilTemplate, reconhecimentosDoColaborador);

				administradorHelper.mostrarConteudoSeForAdministrador('div[data-js="switch-adm"]');

				switchAdministrador(reconhecimentosDoColaborador, colaboradorId);

				$("#conteudo").on(
					"click",
					'div[data-js="exibir-reconhecimentos"]',
					exibirReconhecimentos
				);

				if (sessaoDeUsuario.id === colaboradorId) {
					$('div[data-js="switch-adm"]').hide();
					$("span.ion-camera").show();
					$("#conteudo").on(
						"click",
						'div[data-js="foto"]',
						abrirModalCrop
					);
					
					$('input[data-js="alterar-foto"]').off().on("change", alterarFoto);
				} else {
					$('div[data-js="apreciacao"]').show();
					$('div[data-js="foto"]').removeClass("alterar-foto");
				}

			$('#conteudo')
				.on('click', 'div[data-js="exibir-reconhecimentos"]', exibirReconhecimentos);

			if (sessaoDeUsuario.id === colaboradorId) {
				$('div[data-js="switch-adm"]').hide();
				$('span.ion-camera').show();
				$('#conteudo').on('click', 'div[data-js="foto"]', abrirModalCrop);
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
		$("#conteudo").off();
	};

	function abrirModalCrop(){
		document.getElementById('caixa-modal').style.display= "block";
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

		require(["roteador"], function (roteador) {
			var pilarId = objetoClicado.data("pilar-id");
			var colaboradorId = $("#reconhecidoId").val();

			roteador.navegarPara("/reconhecimentos/" + colaboradorId + "/" + pilarId);
		});
	}

	function confirmaAlteracao() {
		if (confirm("Confirmar as alteracoes?") && administradorHelper.ehAdministrador()) {
			return true;
		} else {
			return false;
		}
	}

	function switchAdministrador(reconhecimentosDoColaborador, colaboradorId) {
		if (reconhecimentosDoColaborador.administrador === true) {
			document.getElementById("toggle").checked = true;
		} else {
			document.getElementById("toggle").checked = false;
		}
		$("#toggle").change(function () {
			if (administradorHelper.ehAdministrador()) {
				if (this.checked) {
					if (confirmaAlteracao()) {
						var dados = {
							id_do_colaborador: colaboradorId,
							eh_administrador: true,
						};
						var mensagem = "Colaborador se tornou um administrador com sucesso!";

						postSwitch(dados, mensagem);
					} else {
						$("#toggle").prop("checked", false);
					}
				}
				else {
					if (confirmaAlteracao()) {
						var dados = {
							id_do_colaborador: colaboradorId,
							eh_administrador: false,
						};
						var mensagem = "Retirado o acesso de administrador do Colaborador com sucesso!";

						postSwitch(dados, mensagem);
					} else {
						$("#toggle").prop("checked", true);
					}
				}
			}
		});
	}

	function postSwitch(dados, mensagem) {
		$.post("/reconhecimentos/administrador/", dados).done(function () {
			require(["growl"], function (growl) {
				growl.deSucesso().exibir(mensagem);
			});
		});
	}

	// TODO: Modular esse envio de foto e aliar com webcomponent
	function abrirSelecaoDeImagens() {
		$('input[data-js="alterar-foto"]').trigger("click");
	}

	function alterarFoto() {
		var arquivo = this.files[0];

		if (arquivo.size > 2621440)
			throw new ViolacaoDeRegra(
				"A sua foto pode ter no máximo 2,5 MB de tamanho"
			);

		if (arquivo.type.indexOf("image/") === -1)
			throw new ViolacaoDeRegra(
				"Apenas imagens podem ser enviadas para seu perfil"
			);

		var reader = new FileReader();

		reader.onload = function (progressEvent) {
			var nova_imagem = $('#imagem__cortada').src;
			var data = {
				id_do_colaborador: sessaoDeUsuario.id,
				nova_foto: reader.result,
			};
			
			
			$.post("/login/alterar_foto/", data)
				.done(function () {
					$('img[data-js="foto"]').attr("src", reader.result);
					$('div[data-js="meu-perfil"] img').attr("src", reader.result);
				})
				.fail(function () {
					require(["growl"], function (growl) {
						growl.deErro().exibir("Não foi possível alterar sua foto :(");
					});
				});
		};

		if (arquivo) reader.readAsDataURL(arquivo);
	}

	return _self;
});
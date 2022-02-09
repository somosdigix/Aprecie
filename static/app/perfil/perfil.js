define([
	"jquery",
	"template",
	"text!app/perfil/perfilTemplate.html",
	"sessaoDeUsuario",
], function ($, template, perfilTemplate, sessaoDeUsuario) {
	"use strict";

	var _self = {};
	var _sandbox;

	_self.inicializar = function (sandbox, colaboradorId) {
		_sandbox = sandbox;

		$.getJSON(
			"/reconhecimentos/colaborador/" + colaboradorId,
			function (reconhecimentosDoColaborador) {
				template.exibir(perfilTemplate, reconhecimentosDoColaborador);

				mostraSwitchAdministrador(sessaoDeUsuario.administrador);

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
						abrirSelecaoDeImagens
					);
					$('input[data-js="alterar-foto"]').off().on("change", alterarFoto);
					obterNotificacaoDoAdministrador();
				} else {
					$('div[data-js="apreciacao"]').show();
					$('div[data-js="foto"]').removeClass("alterar-foto");
				}

				_sandbox.notificar(
					"exibir-espaco-para-apreciar",
					colaboradorId,
					reconhecimentosDoColaborador
				);
				_sandbox.notificar("exibir-apreciacoes");
			}
		);
	};

	_self.finalizar = function () {
		$("#conteudo").off();
	};

	function obterStatusDeNotificacao(){
		let statusNotificacao = localStorage.getItem('notificacao');
		return JSON.parse(statusNotificacao);
	}

	function obterNotificacaoDoAdministrador(){
		if(obterStatusDeNotificacao()){
			$.getJSON("/reconhecimentos/obter_notificacoes_administrador/", function(notificacao){
				require(["growl"], function (growl){
					growl.deErro().exibir(notificacao.mensagem);
				})
			})
			localStorage.setItem('notificacao', 'false');
		}
	}

	function exibirReconhecimentos() {
		var objetoClicado = $(this);

		require(["roteador"], function (roteador) {
			var pilarId = objetoClicado.data("pilar-id");
			var colaboradorId = $("#reconhecidoId").val();

			roteador.navegarPara("/reconhecimentos/" + colaboradorId + "/" + pilarId);
		});
	}

	function mostraSwitchAdministrador(administrador) {
		if (administrador === false) {
			$('div[data-js="switch-adm"]').hide();
		} else {
			$('div[data-js="switch-adm"]').show();
		}
	}

	function confirmaAlteracao() {
		if (confirm("Confirmar as alteracoes?") && usuarioAdministrador()) {
			return true;
		} else {
			return false;
		}
	}

	function usuarioAdministrador () {
		if (!sessaoDeUsuario.administrador) {
			require(["growl"], function (growl) {
				growl.deErro().exibir("Você não é administrador");
				return false;
			});
		} else {
			return sessaoDeUsuario.administrador;
		}
	}

	function switchAdministrador(reconhecimentosDoColaborador, colaboradorId) {
		if (reconhecimentosDoColaborador.administrador === true) {
			document.getElementById("toggle").checked = true;
		} else {
			document.getElementById("toggle").checked = false;
		}
		$("#toggle").change(function () {
			if (usuarioAdministrador()) {
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

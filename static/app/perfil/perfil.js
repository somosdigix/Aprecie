define([
	'jquery',
	'template',
	'text!app/perfil/perfilTemplate.html',
	'sessaoDeUsuario',
	'app/botaoReconhecer/botaoReconhecer',
	'app/helpers/administradorHelper',
	'app/helpers/recursosHumanosHelper',
	"growl",
	"roteador"
], function ($, template, perfilTemplate, sessaoDeUsuario, botaoReconhecer, administradorHelper, recursosHumanosHelper, growl, roteador) {
	'use strict';

	var _self = {};
	var _sandbox;

	_self.inicializar = function (sandbox, colaboradorId) {
		_sandbox = sandbox;
		$.getJSON(
			"/reconhecimentos/colaborador/" + colaboradorId,
			function (reconhecimentosDoColaborador) {
				template.exibir(perfilTemplate, reconhecimentosDoColaborador);
				switchAdministrador(reconhecimentosDoColaborador, colaboradorId);

				$("#conteudo").on(
					"click",
					'div[data-js="exibir-reconhecimentos"]',
					exibirReconhecimentos
				);
				if (sessaoDeUsuario.id === colaboradorId) {
					$('div[data-js="switch-adm"]').hide();
					administradorHelper.mostrarConteudoSeForAdministrador('div[data-js="menu__administrador"]');
					configurarMenuAdministrador();

					$("span.ion-camera").show();
					$("#conteudo").on(
						"click",
						'div[data-js="foto"]',
						abrirModalCrop
					);

					$('#conteudo').on('click', 'button[data-js="alterar-foto"]', alterarFoto);
					$('#conteudo').on('click', 'button[data-js="botao_fechar_cropper"]', fecharModalCrop);
					$('#conteudo').on('change', 'input[data-js="input__arquivos"]', readURL);

					if (sessaoDeUsuario.recursos_humanos) {
						recursosHumanosHelper.mostrarConteudoSeForRecursosHumanos('div[data-js="menu__recursos_humanos')
						configurarMenuRecursosHumanos();
					}

					if (sessaoDeUsuario.administrador) {
						administradorHelper.mostrarConteudoSeForAdministrador('div[data-js="menu__administrador"]');
						configurarMenuAdministrador();
						obterNotificacaoDoAdministrador();
					}

					$('#conteudo')
						.on("click", 'button[class="botao--fecharModalAgradecimento"]', fecharModalAdicionarAgradecimento)
						.on("submit", 'form[data-js="form_adicionar_agradecimento"]', agradecer);
				} else {
					if (!sessaoDeUsuario.administrador) {
						$('div[data-js="switch-adm"]').hide();
					}
					$('div[data-js="menu__administrador"]').hide();
					$('div[data-js="apreciacao"]').show();
					$('div[data-js="foto"]').removeClass("alterar-foto");
				}

				$('#conteudo')
					.on('click', 'button[data-js="exibir-reconhecimentos"]', exibirReconhecimentos);

				if (sessaoDeUsuario.id === colaboradorId) {
					$('div[data-js="switch-adm"]').hide();
					$('span.ion-camera').show();
					$('#conteudo').on('click', 'div[data-js="foto"]', abrirModalCrop);
					$('#conteudo').on('click', 'button[data-js="alterar-foto"]', alterarFoto);
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

	function rankingAdmin() {
		require(['roteador'], function (roteador) {
			roteador.navegarPara('/rankingAdmin');
		});
	}

	function gerenciadorDeCiclos() {
		require(['roteador'], function (roteador) {
			roteador.navegarPara('/gerenciadorDeCiclos');
		});
	}

	function logAdministrador() {
		require(['roteador'], function (roteador) {
			roteador.navegarPara('/logAdministrador');
		});
	}
	function casdastroRH() {
		require(['roteador'], function (roteador) {
			roteador.navegarPara('/cadastroDeColaboradores');
		});
	}
	function ListagemRH() {
		require(['roteador'], function (roteador) {
			roteador.navegarPara('/listagemColaboradoresRh');
		});
	}

	function configurarMenuAdministrador() {
		$("#conteudo")
			.on('click', 'a[data-js="ranking-admin"]', rankingAdmin)
			.on('click', 'a[data-js="configuracao-ciclo"]', gerenciadorDeCiclos)
			.on('click', 'a[data-js="logs-administrador"]', logAdministrador);
	}

	function configurarMenuRecursosHumanos() {
		$("#conteudo")
			.on('click', 'a[data-js="cadastro-recursos_humanos"]', casdastroRH)
		$("#conteudo")
			.on('click', 'a[data-js="listagem-recursos_humanos"]', ListagemRH)
	}

	function abrirModalCrop() {
		document.getElementById('caixa-modal').style.display = "block";
	}

	function fecharModalCrop() {
		document.getElementById('caixa-modal').style.display = "none";
	}

	function fecharModalAdicionarAgradecimento() {
		document.getElementById('modal__adicionar-agradecimento').style.display = "none";
	}

	function agradecer(event) {
		event.preventDefault();
		var data = {
			'id_reconhecimento_vinculado': $('#id_reconhecimento_vinculado').val(),
			'id_colaborador_que_agradeceu': $('#id_colaborador_que_agradeceu').val(),
			'agradecimento': $('#agradecimento').val(),
		}

		$.post('/reconhecimentos/agradecer/', data, function () {
			growl.deSucesso().exibir('Agradecimento feito com sucesso');
			roteador.atualizar();
		})
	};

	function obterStatusDeNotificacao() {
		let statusNotificacao = localStorage.getItem('notificacao');
		return JSON.parse(statusNotificacao);
	}

	function obterNotificacaoDoAdministrador() {
		if (obterStatusDeNotificacao()) {
			$.getJSON("/reconhecimentos/obter_notificacoes_administrador/", function (notificacao) {
				require(["growl"], function (growl) {
					if (notificacao.mensagem != " ") {
						growl.deErro().exibir(notificacao.mensagem);
					}
				})
			})
			localStorage.setItem('notificacao', 'false');
		}
	}

	function apreciar() {
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
			console.log("entrou!")
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
		$.post("/login/administrador/", dados).done(function () {
			require(["growl"], function (growl) {
				growl.deSucesso().exibir(mensagem);
			});
		});
	}

	function alterarFoto() {
		var nova_imagem = document.getElementById('url_imagem_cortada').innerHTML;
		var data = {
			id_do_colaborador: sessaoDeUsuario.id,
			nova_foto: nova_imagem,
		};

		$.post("/login/alterar_foto/", data)
			.done(function () {
				$('img[data-js="foto"]').attr("src", nova_imagem);
				$('div[data-js="meu-perfil"] img').attr("src", nova_imagem);
			})
			.fail(function () {
				require(["growl"], function (growl) {
					growl.deErro().exibir("Não foi possível alterar sua foto :(");
				});
			});

		fecharModalCrop();
	}

	function readURL() {
		var arquivo = this.files[0];

		if (arquivo.size > 2621440)
			throw new ViolacaoDeRegra(
				"A sua foto pode ter no máximo 2,5 MB de tamanho"
			);

		if (arquivo.type.indexOf("image/") === -1)
			throw new ViolacaoDeRegra(
				"Apenas imagens podem ser enviadas para seu perfil"
			);

		if (this.files && this.files[0]) {
			var reader = new FileReader();

			reader.onload = function (e) {
				document.getElementById("imagem__selecionada__container").innerHTML = "<img id='imagem__selecionada' src=" + e.target.result + " alt='imagem selecionada'/>"
			};

			if (arquivo) reader.readAsDataURL(arquivo);

			setTimeout(initCropper, 10);
			document.querySelector("#imagem__botao__cropper").style.display = "block";
		}
	}

	return _self;
});

function abrirModalAdicionarAgradecimento(idReconhecimento, idColaborador) {
	document.getElementById('modal__adicionar-agradecimento').style.display = "block";
	var inputIdReconhecimento = document.getElementById('id_reconhecimento_vinculado');
	inputIdReconhecimento.value = idReconhecimento;

	var inputIdColaborador = document.getElementById('id_colaborador_que_agradeceu');
	inputIdColaborador.value = idColaborador;
}
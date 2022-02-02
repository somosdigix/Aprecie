define([
	"jquery",
	"template",
	"text!app/botaoReconhecer/botaoReconhecerTemplate.html",
	"sessaoDeUsuario",
	"app/models/reconhecerGlobalViewModel",
	"growl",
	"roteador",
	"text!app/botaoReconhecer/modalReconhecer.html"
], function (
	$,
	template,
	botaoReconhecerTemplate,
	sessaoDeUsuario,
	ReconhecerGlobalViewModel,
	growl,
	roteador,
	modalReconhecerTemplate
) {
	"use strict";

	var botaoReconhecer = {};
	var contagemCaracteres = 0;
	var colaboradoresEPilaresModal = {}

	botaoReconhecer.exibir = function (callback) {

		if ($('div[data-js="botaoReconhecer"]').html() == '') {
			$.getJSON("/reconhecimentos/pilares", function (colaboradoresEPilares) {
				template.exibirEm(
					'div[data-js="botaoReconhecer"]',
					botaoReconhecerTemplate,
				);

				colaboradoresEPilaresModal = colaboradoresEPilares

				$("#global")
					.on(
						"click",
						'button[data-js="abrir-modal"]',
						botaoReconhecer.exibirModal
					)
					.on(
						"click",
						'button[data-js="fechar-modal"]',
						botaoReconhecer.fecharModal
					)
					.on("keyup", 'textarea[data-js="mostrar-contagem"]', mostrarContagem)
					.on(
						"click",
						"div.conteudo-botaoReconhecer div.campoGlobal",
						selecionarPilarGlobal
					)
					.on("click", 'button[data-js="reconhecerGlobal"]', botaoReconhecer.reconhecerGlobal);
					
				$('div[data-js="botaoReconhecer"]').show();


				if (callback) callback();
			});
		}
	};

	botaoReconhecer.esconder = function () {
		$('div[data-js="botaoReconhecer"]').hide(botaoReconhecerTemplate).empty();
	};

	botaoReconhecer.exibirModal = function () {
		template.exibirEm('div[data-js="modalReconhecer"]', modalReconhecerTemplate, colaboradoresEPilaresModal);

		$('div[data-js="buscaColaboradores"]').search({
			source: converterParaAutocomplete(colaboradoresEPilaresModal.colaboradores),
			onSelect: botaoReconhecer.selecionarReconhecido,
			error: {
				noResults: "Nenhum colaborador foi encontrado.",
			},
		});
	};

	botaoReconhecer.fecharModal = function () {
		$(".modalReconhecer").hide();
	};

	function converterParaAutocomplete(colaboradores) {
		return colaboradores.map(function (colaborador) {
			colaborador.title = colaborador.nome;

			return colaborador;
		});
	}

	function selecionarPilarGlobal() {
		$("div.campoGlobal.selecionadoGlobal").removeClass("selecionadoGlobal");
		$(this)
			.toggleClass("selecionadoGlobal")
			.find(".inputPilar")
			.attr("checked", true);
	}

	botaoReconhecer.reconhecerGlobal = function () {
		$('button[data-js="reconhecerGlobal"]').prop("disabled", "disabled");

		var reconhecerGlobalViewModel = new ReconhecerGlobalViewModel();

		try {
			validarOperacao(reconhecerGlobalViewModel);
		} catch (erro) {
			$('#global button[data-js="reconhecerGlobal"]').removeAttr("disabled");
			throw erro
		}

		$.post("/reconhecimentos/reconhecer/", reconhecerGlobalViewModel, function () {
			growl.deSucesso().exibir("Reconhecimento realizado com sucesso.");
		}).fail(function () {
			$('#conteudo button[data-js="reconhecerGlobal"]').removeAttr("disabled");
		});

		setTimeout(() => {
			window.location.reload(true);
		}, 750);
	}

	function validarOperacao(reconhecerViewModel) {
		if (!reconhecerViewModel.id_do_pilar)
			throw new ViolacaoDeRegra("O pilar deve ser informado");

		if (reconhecerViewModel.descritivo === "")
			throw new ViolacaoDeRegra(
				"O motivo do reconhecimento deve ser informado"
			);

		if (reconhecerViewModel.id_do_reconhecido == sessaoDeUsuario.id) {
			throw new ViolacaoDeRegra(
				"Não é possível se auto reconhecer, selecione a pessoa que você queira reconhecer"
			);
		}
	}

	botaoReconhecer.selecionarReconhecido = function (colaborador) {
		document
			.getElementById("idDoReconhecido")
			.setAttribute("value", colaborador.id_colaborador);

		$('div[data-js="buscaColaboradores"]').search(
			"set value",
			colaborador.nome
		);
	};

	function mostrarContagem() {
		var box = $(".elogio");
		var contagemCaracteres = box.val().length;
		var limiteDeCaracteres = parseInt(box.attr("maxlength"));
		var campospan = document.getElementById("spcontando");

		campospan.innerHTML = contagemCaracteres + "/" + limiteDeCaracteres;

		if (contagemCaracteres >= limiteDeCaracteres) {
			campospan.innerHTML = "Limite de caracteres excedido!";
		}
	}

	return botaoReconhecer;
});

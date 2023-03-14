define([
	"jquery",
	"template",
	"text!app/botaoReconhecer/botaoReconhecerTemplate.html",
	"sessaoDeUsuario",
	"app/models/reconhecerGlobalViewModel",
	"growl",
	"text!app/botaoReconhecer/modalReconhecer.html"
], function (
	$,
	template,
	botaoReconhecerTemplate,
	sessaoDeUsuario,
	ReconhecerGlobalViewModel,
	growl,
	modalReconhecerTemplate
) {
	"use strict";

	var botaoReconhecer = {};
	var colaboradoresEPilaresModal = {}

	botaoReconhecer.exibir = function (callback) {
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

		let buscaInput = document.querySelector("#busca-botaoReconhecer");
		buscaInput.addEventListener('keyup', () => {
			buscaInput.value = remover_acentos_espaco(buscaInput.value);
		})
	};

	botaoReconhecer.fecharModal = function () {
		$(".modalReconhecer").hide();
	};

	botaoReconhecer.existe = function () {
		return !($('div[data-js="botaoReconhecer"]').html() == '');
	}

	function converterParaAutocomplete(colaboradores) {
		return colaboradores.map(function (colaborador) {
			colaborador.title = remover_acentos_espaco(colaborador.nome);
			return colaborador;
		});
	}

	function remover_acentos_espaco(str) {
		return str.normalize("NFD").replace(/[^a-zA-Z\s]/g, "");
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
		}, 5000);
	}


	function reconhecerGlobal() {
		$('button[data-js="reconhecerGlobal"]').prop("disabled", "disabled");
		obterDataDeReconhecimento();
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


function mostrarResultado(box, limiteDeCaracteres, campospan) {
	var contagemCaracteres = box.length;

	if (contagemCaracteres >= 0) {
		document.getElementById(campospan).innerHTML = contagemCaracteres + "/220";
	}
	if (contagemCaracteres >= limiteDeCaracteres) {
		document.getElementById(campospan).innerHTML = "Limite de caracteres excedido!";
	}
}


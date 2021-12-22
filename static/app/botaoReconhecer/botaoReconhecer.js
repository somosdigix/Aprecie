define([
	"jquery",
	"template",
	"text!app/botaoReconhecer/botaoReconhecerTemplate.html",
	"sessaoDeUsuario",
	"app/models/reconhecerGlobalViewModel",
	"growl",
	"roteador",
	"jquery-ui",
], function (
	$,
	template,
	botaoReconhecerTemplate,
	sessaoDeUsuario,
	ReconhecerGlobalViewModel,
	growl,
	roteador
) {
	"use strict";

	var botaoReconhecerView = {};

	botaoReconhecerView.exibir = function (callback) {
		$.getJSON("/reconhecimentos/pilares", function (colaboradoresEPilares) {
			template.exibirEm(
				'div[data-js="botaoReconhecer"]',
				botaoReconhecerTemplate,
				colaboradoresEPilares
			);

			$("#global")
				.on(
					"click",
					"div.conteudo-botaoReconhecer div.campoGlobal",
					selecionarPilarGlobal
				)
				.on("click", 'button[data-js="reconhecerGlobal"]', reconhecerGlobal);

			$('div[data-js="botaoReconhecer"]').show();
			$(".modalReconhecer").hide();

			$('div[data-js="buscaColaboradores"]').search({
				source: converterParaAutocomplete(colaboradoresEPilares.colaboradores),
				onSelect: selecionarReconhecido,
				error: {
					noResults: "Não encontrei ninguém :(",
				},
			});

			if (callback) callback();
		});
	};

	botaoReconhecerView.esconder = function () {
		$('div[data-js="botaoReconhecer"]').hide(botaoReconhecerTemplate).empty();
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

	async function reconhecerGlobal() {
		$('button[data-js="reconhecerGlobal"]').prop("disabled", "disabled");
		var reconhecerGlobalViewModel = new ReconhecerGlobalViewModel();
		
		try {
			validarOperacao(reconhecerGlobalViewModel);
		} catch (erro) {
			$('#global button[data-js="reconhecerGlobal"]').removeAttr("disabled");
			throw erro;
		}

		await $.post("/reconhecimentos/reconhecer/", reconhecerGlobalViewModel, function () {
			growl.deSucesso().exibir("Reconhecimento realizado com sucesso");
		}).fail(function () {
			$('#global button[data-js="reconhecerGlobal"]').removeAttr("disabled");
		});

		window.location.reload(true);
	}

	function validarOperacao(reconhecerViewModel) {
		if (!reconhecerViewModel.id_do_pilar)
			throw new ViolacaoDeRegra("O pilar deve ser informado");

		if (reconhecerViewModel.descritivo === "")
			throw new ViolacaoDeRegra(
				"O descritivo da sua apreciação precisa ser informado"
			);

		if (reconhecerViewModel.id_do_reconhecido == sessaoDeUsuario.id) {
			throw new ViolacaoDeRegra("Você não pode se apreciar");
		}
	}

	function selecionarReconhecido(colaborador) {
		var divReconhecido = $('div[data-js="buscaColaboradores"]');
		document
			.getElementById("idDoReconhecido")
			.setAttribute("value", colaborador.id_colaborador);
		divReconhecido.value = colaborador.nome;
	}

	return botaoReconhecerView;
});

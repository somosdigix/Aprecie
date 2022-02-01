define([
	"jquery",
	"template",
	"text!app/botaoReconhecer/botaoReconhecerTemplate.html",
	"sessaoDeUsuario",
	"app/models/reconhecerGlobalViewModel",
	"growl",
	"roteador",
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

	var botaoReconhecer = {};
	var contagemCaracteres = 0;

	botaoReconhecer.exibir = function (callback) {
		$.getJSON("/reconhecimentos/pilares", function (colaboradoresEPilares) {
			template.exibirEm(
				'div[data-js="botaoReconhecer"]',
				botaoReconhecerTemplate,
				colaboradoresEPilares
			);

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
				.on("click", 'button[data-js="reconhecerGlobal"]', reconhecerGlobal);

			$('div[data-js="botaoReconhecer"]').show();
			$(".modalReconhecer").hide();

			$('div[data-js="buscaColaboradores"]').search({
				source: converterParaAutocomplete(colaboradoresEPilares.colaboradores),
				onSelect: botaoReconhecer.selecionarReconhecido,
				error: {
					noResults: "Nenhum colaborador foi encontrado.",
				},
			});

			if (callback) callback();
		});
	};

	botaoReconhecer.esconder = function () {
		$('div[data-js="botaoReconhecer"]').hide(botaoReconhecerTemplate).empty();
	};

	botaoReconhecer.exibirModal = function () {
		$(".modalReconhecer").show();
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

	function reconhecerGlobal() {
		$('button[data-js="reconhecerGlobal"]').prop("disabled", "disabled");
		var reconhecerGlobalViewModel = new ReconhecerGlobalViewModel();

		try {
			validarOperacao(reconhecerGlobalViewModel);
		} catch (erro) {
			$('#global button[data-js="reconhecerGlobal"]').removeAttr("disabled");
			throw erro;
		}

		$.post("/reconhecimentos/reconhecer/", reconhecerGlobalViewModel, function () {
			growl.deSucesso().exibir("Reconhecimento realizado com sucesso.");
		}).fail(function () {
			$('#conteudo button[data-js="reconhecerGlobal"]').removeAttr("disabled");
		});
		
		roteador.atualizar();
		// setTimeout(() => {
		// 	window.location.reload(true);
		// }, 750);
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

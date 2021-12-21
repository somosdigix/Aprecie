define([
	"jquery",
	"template",
	"text!app/botaoReconhecer/botaoReconhecerTemplate.html",
	"sessaoDeUsuario",
	"app/models/reconhecerGlobalViewModel",
	"growl",
	"roteador",
	"jquery-ui",
], function ($, template, botaoReconhecerTemplate, sessaoDeUsuario, ReconhecerGlobalViewModel, growl, roteador,) {
	"use strict";

	var botaoReconhecerView = {};

	botaoReconhecerView.exibir = function (callback) {
		$.getJSON("/login/obter_colaboradores/", function (data) {
			template.exibirEm(
				'div[data-js="botaoReconhecer"]',
				botaoReconhecerTemplate,
				sessaoDeUsuario
			);

			$("#global")
				.on(
					"click",
					"div.conteudo-botaoReconhecer div.escolhaPilar",
					selecionarPilar
				)
				.on("click", 'button[data-js="reconhecerGlobal"]', reconhecerGlobal);

			$('div[data-js="botaoReconhecer"]').show();

			$('div[data-js="buscaColaboradores"]').search({
				source: converterParaAutocomplete(data.colaboradores),
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

	function selecionarPilar() {
		$("div.escolhaPilar.selecionado").removeClass("selecionado");
		$(this).toggleClass("selecionado").find(":radio").attr("checked", true);
	}

	function reconhecerGlobal() {
		console.log("oi");
		var reconhecerGlobalViewModel = new ReconhecerGlobalViewModel();

		try {
			validarOperacao(reconhecerGlobalViewModel);
		} catch (erro) {
			throw erro;
		}

		$.post(
			"/reconhecimentos/reconhecer/",
			reconhecerGlobalViewModel,
			function () {
				growl.deSucesso().exibir("Reconhecimento realizado com sucesso");
				roteador.atualizar();
			}
		);
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
			.setAttribute("value", colaborador.id);
		divReconhecido.value = colaborador.nome;
	}

	return botaoReconhecerView;
});

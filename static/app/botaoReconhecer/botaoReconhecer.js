define([
	"jquery",
	"template",
	"text!app/botaoReconhecer/botaoReconhecerTemplate.html",
	"sessaoDeUsuario",
	"app/models/reconhecerGlobalViewModel",
	"growl",
	"app/helpers/formatadorDeData"
], function (
	$,
	template,
	botaoReconhecerTemplate,
	sessaoDeUsuario,
	ReconhecerGlobalViewModel,
	growl,
	formatadorDeData
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
					noResults: "Nenhum colaborador foi encontrado.",
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

	function gerarReconhecimento(){
		var reconhecerGlobalViewModel = new ReconhecerGlobalViewModel();

		try {
			validarOperacao(reconhecerGlobalViewModel);
		} catch (erro) {
			$('#global button[data-js="reconhecerGlobal"]').removeAttr("disabled");
			throw erro;
		}

		$.post("/reconhecimentos/reconhecer/", reconhecerGlobalViewModel, function () {
			growl.deSucesso().exibir("Reconhecimento realizado com sucesso");
		}).fail(function () {
			$('#global button[data-js="reconhecerGlobal"]').removeAttr("disabled");
		});

		window.location.reload(true);
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
			throw new ViolacaoDeRegra("Não é possível se auto reconhecer, selecione a pessoa que você queira reconhecer");
		}
	}

	function selecionarReconhecido(colaborador) {
		var divReconhecido = $('div[data-js="buscaColaboradores"]');
		document
			.getElementById("idDoReconhecido")
			.setAttribute("value", colaborador.id_colaborador);
		divReconhecido.value = colaborador.nome;
	}

	function obterDataDeReconhecimento() {
		var dataHoje = formatadorDeData.obterHoje("-");
		$.getJSON(
			"/reconhecimentos/ultima_data_de_publicacao/" + sessaoDeUsuario.id,
			function (dataDePublicacao) {
				if (dataDePublicacao.ultima_data == null || dataDePublicacao.ultima_data < dataHoje) {
					gerarReconhecimento();
				} else if (dataDePublicacao.ultima_data == dataHoje) {
					growl
						.deErro()
						.exibir(
							"Você já fez seu reconhecimento de hoje, amanhã você poderá fazer outro"
						);
						setTimeout(() => {
							window.location.reload(true)}, 500);
				}
			}
		);
	}

	return botaoReconhecerView;
});

function mostrarResultado(box, numeroMaximo, campospan){
	var quantidadeDeCaracteres = box.length;
	
	if (quantidadeDeCaracteres >= 0){
		document.getElementById(campospan).innerHTML = quantidadeDeCaracteres + "/220";
	}

	if (quantidadeDeCaracteres >= numeroMaximo){
		document.getElementById(campospan).innerHTML = "Limite de caracteres excedido!";
	}
}
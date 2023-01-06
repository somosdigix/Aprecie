define([
	"jquery",
	"template",
	"text!app/rankingAdmin/rankingAdminTemplate.html",
	"text!app/rankingAdmin/rankingAdmin.html",
	"text!app/rankingAdmin/filtrosRankingAdminTemplate.html",
	'app/models/filtroDataAdminViewModel',
	"app/helpers/formatadorDeData",
	"app/helpers/administradorHelper",
	'roteador',
], function ($, template, rankingAdminTemplate, rankingAdmin, filtrosRankingAdminTemplate, FiltroDataAdminViewModel, formatadorDeData, administradorHelper, roteador) {
	"use strict";

	var self = {};
	var _sandbox;
	var ranking_colaboradores;


	self.inicializar = function (sandbox) {
		_sandbox = sandbox;

		if (administradorHelper.ehAdministrador()) {
			template.exibir(rankingAdminTemplate);
			carregarFiltrosRankingAdmin();
			carregarRankingAdmin();

			$('#conteudo')
				.on('click', 'input[data-js="todos"]', ordenaRankingPorPilar)
				.on('click', 'input[data-js="feitos"]', ordenaRankingPorPilar)
				.on('click', 'input[data-js="colaborarSempre"]', ordenaRankingPorPilar)
				.on('click', 'input[data-js="focarNasPessoas"]', ordenaRankingPorPilar)
				.on('click', 'input[data-js="fazerDiferente"]', ordenaRankingPorPilar)
				.on('click', 'input[data-js="planejarEntregarAprender"]', ordenaRankingPorPilar)
				.on('click', 'button[data-js="botao__ranking__adm"]', carregarRankingPeriodoDeDatas);

			$.getJSON('/login/obter_colaboradores/', function (data) {

				$('div[data-js="buscarColaboradorRanking"]').search({
					source: converterParaAutocomplete(data.colaboradores),
					onSelect: ordenaRankingPorNome,
					error: {
						noResults: 'Não encontrei ninguém :('
					}
				});

				let buscaInput = document.querySelector("#input_busca_colaborador_ranking");
				buscaInput.addEventListener('keyup', () => {
					buscaInput.value = remover_acentos_espaco(buscaInput.value);
				})
			});
		}
		else {
			roteador.navegarPara('/paginaInicial');
		}

	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};


	function carregarFiltrosRankingAdmin() {
		template.exibirEm('div[data-js="container__filtros__ranking"]', filtrosRankingAdminTemplate);
	}

	function carregarRankingAdmin() {
		var dataHoje = formatadorDeData.obterHoje("-");
		var data = {
			'data_inicio': dataHoje,
			'data_fim': dataHoje
		}

		criarRankingPorPeriodo(data);
		document.getElementById('data_inicial').value = dataHoje;
		document.getElementById('data_final').value = dataHoje;
	}

	function carregarRankingPeriodoDeDatas() {
		var filtroDataAdminViewModel = new FiltroDataAdminViewModel()
		criarRankingPorPeriodo(filtroDataAdminViewModel);
	}

	function criarRankingPorPeriodo(dataAdminViewModel) {
		$.post("/reconhecimentos/ranking_por_periodo/", dataAdminViewModel, function (ranking_de_colaboradores) {
			ranking_colaboradores = ranking_de_colaboradores;
			var busca_por_nome = $("#input_busca_colaborador_ranking").val();
			if (busca_por_nome != '') {
				var rankingPorNome = filtrarNome(ranking_de_colaboradores, busca_por_nome);
				exibirRanking(rankingPorNome);
			}
			else {
				exibirRanking(ranking_de_colaboradores.colaboradores);
				ordenaRankingPorPilar();
			}
		});
	}

	function exibirRanking(ranking_de_colaboradores) {
		template.exibirEm('div[data-js="container__ranking"]', rankingAdmin, ranking_de_colaboradores);
		posicaoDinamica();

		var busca_por_nome = $("#input_busca_colaborador_ranking").val();
		if (busca_por_nome == '') {
			var titulo = $("input[name=filtro__pilares__ranking]:checked").attr("pilar_ranking");
			document.getElementById("ranking__admin__pilar").innerHTML = titulo;
		}
	}

	function ordenaRankingPorPilar() {
		var rankingPorPilar = jQuery.extend(true, {}, ranking_colaboradores);

		var pilarSelecionado = $("input[name=filtro__pilares__ranking]:checked").val();

		if (pilarSelecionado != 'todos_reconhecimentos') {
			rankingPorPilar.colaboradores.sort(function (colaborador1, colaborador2) {
				return verificaValorDoPilar(colaborador2, pilarSelecionado) - verificaValorDoPilar(colaborador1, pilarSelecionado);
			});
		}

		exibirRanking(rankingPorPilar.colaboradores);
	}

	function verificaValorDoPilar(colaborador, pilarSelecionado) {
		if (pilarSelecionado == 'colaborar_sempre') {
			return colaborador.colaborar_sempre;
		}
		else if (pilarSelecionado == 'focar_nas_pessoas') {
			return colaborador.focar_nas_pessoas;
		}
		else if (pilarSelecionado == 'fazer_diferente') {
			return colaborador.fazer_diferente;
		}
		else if (pilarSelecionado == 'planejar_entregar_aprender') {
			return colaborador.planejar_entregar_aprender;
		}
		else if (pilarSelecionado == 'reconhecimentos_feitos') {
			return colaborador.reconhecimentos_feitos;
		}
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

	function ordenaRankingPorNome(colaborador) {
		var rankingPorNome = jQuery.extend(true, {}, ranking_colaboradores);

		var colaboradorFiltrado = filtrarNome(rankingPorNome, colaborador.nome);

		exibirRanking(colaboradorFiltrado);
	}

	function filtrarNome(rankingPorNome, nomeColaborador) {
		return rankingPorNome.colaboradores.filter(function (colaborador) {
			if (colaborador.nome.toLowerCase() === nomeColaborador.toLowerCase()) {
				return colaborador;
			}
		})
	}

	function posicaoDinamica() {
		var ranking = document.getElementsByClassName('posicao__ranking__admin');
		for (var i = 0; i < ranking.length; i++) {
			ranking[i].innerHTML = (i + 1) + ' ºlugar';
		}
	}

	return self;
});
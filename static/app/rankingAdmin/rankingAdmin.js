define([
	"jquery",
	"template",
	"text!app/rankingAdmin/rankingAdminTemplate.html",
	"text!app/rankingAdmin/rankingAdmin.html",
	"text!app/rankingAdmin/filtrosRankingAdminTemplate.html",
	'app/models/filtroDataAdminViewModel'
], function ($, template, rankingAdminTemplate, rankingAdmin, filtrosRankingAdminTemplate, FiltroDataAdminViewModel) {
	"use strict";

	var self = {};
	var _sandbox;
	var ranking_colaboradores;

	
	self.inicializar = function (sandbox) {
		_sandbox = sandbox;

		template.exibir(rankingAdminTemplate);
		carregarFiltrosRankingAdmin();
		carregarRankingAdmin();

		$('#conteudo')
		.on('click', 'input[data-js="todos"]', ordenaRankingPorPilar)
		.on('click', 'input[data-js="colaborarSempre"]', ordenaRankingPorPilar)
		.on('click', 'input[data-js="focarNasPessoas"]', ordenaRankingPorPilar)
		.on('click', 'input[data-js="fazerDiferente"]', ordenaRankingPorPilar)
		.on('click', 'input[data-js="planejarEntregarAprender"]', ordenaRankingPorPilar)
		.on('click', 'button[data-js="botao__ranking__adm"]', carregarRankingPeriodoDeDatas);

	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};


	function carregarFiltrosRankingAdmin() {
		template.exibirEm('div[data-js="container__filtros__ranking"]', filtrosRankingAdminTemplate);
	}

	function carregarRankingAdmin() {
		// #TODO -> Arrumar as datas de acordo com o metodo obterData() que esta em PR [Apreciacao por dia];
		var data = {
			'data_inicio': "2022-01-07",
			'data_fim': "2022-01-07"
		}
		criarRankingPorPeriodo(data);		
	}
	
	function carregarRankingPeriodoDeDatas() {
		var filtroDataAdminViewModel = new FiltroDataAdminViewModel()
		criarRankingPorPeriodo(filtroDataAdminViewModel);
		ordenaRankingPorPilar();
	}

	function criarRankingPorPeriodo(dataAdminViewModel) {
		$.post("/reconhecimentos/ranking_por_periodo/", dataAdminViewModel , function (ranking_de_colaboradores) {
			ranking_colaboradores = ranking_de_colaboradores;
			
			exibirRanking(ranking_de_colaboradores);
		});
	}

	function exibirRanking(ranking_de_colaboradores){

		template.exibirEm('div[data-js="container__ranking"]', rankingAdmin , ranking_de_colaboradores);
		posicaoDinamica();
		
		var titulo = $("input[name=filtro__pilares__ranking]:checked").attr("pilar_ranking");
		document.getElementById("ranking__admin__pilar").innerHTML = titulo;
	}

	function ordenaRankingPorPilar(){
		var ranking_por_pilar = jQuery.extend(true, {}, ranking_colaboradores);
		
		var pilar_selecionado = $("input[name=filtro__pilares__ranking]:checked").val();

		if (pilar_selecionado != 'todos_reconhecimentos'){
			ranking_por_pilar.colaboradores.sort(function(colaborador1, colaborador2){
				return verificaValorDoPilar(colaborador2) - verificaValorDoPilar(colaborador1);
			});
		}

		exibirRanking(ranking_por_pilar);
	}

	function verificaValorDoPilar(colaborador){
		var pilar_selecionado = $("input[name=filtro__pilares__ranking]:checked").val();
		if(pilar_selecionado == 'colaborar_sempre'){
			return colaborador.colaborar_sempre;
		}
		else if(pilar_selecionado == 'focar_nas_pessoas'){
			return colaborador.focar_nas_pessoas;
		}
		else if(pilar_selecionado == 'fazer_diferente'){
			return colaborador.fazer_diferente;
		}
		else if(pilar_selecionado == 'planejar_entregar_aprender'){
			return colaborador.planejar_entregar_aprender;
		}
	}

	function posicaoDinamica() {
		var ranking = document.getElementsByClassName('posicao__ranking__admin');
		for (var i = 0; i < ranking.length; i++) {
			ranking[i].innerHTML = (i+1)+ ' ºlugar';
		}
	}

	return self;
});
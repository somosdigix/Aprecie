define([
	"jquery",
	"template",
	"text!app/rankingAdmin/rankingAdminTemplate.html",
	"text!app/rankingAdmin/rankingAdmin.html",
	"text!app/rankingAdmin/filtrosRankingAdminTempleate.html",
	'app/models/filtroDataAdminViewModel'
], function ($, template, rankingAdminTemplate, rankingAdmin, filtrosRankingAdminTempleate, FiltroDataAdminViewModel) {
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
		.on('click', 'input[data-js="colaborarSempre"]', carregarRankingPilar)
		.on('click', 'input[data-js="focarNasPessoas"]', carregarRankingPilar)
		.on('click', 'input[data-js="fazerDiferente"]', carregarRankingPilar)
		.on('click', 'input[data-js="planejarEntregarAprender"]', carregarRankingPilar)
		.on('click', 'button[data-js="botao__ranking__adm"]', carregarRankingPeriodoDeDatas);

	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};


	function carregarFiltrosRankingAdmin() {
		template.exibirEm('div[data-js="container__filtros__ranking"]', filtrosRankingAdminTempleate);
	}

	function carregarRankingAdmin() {
		// #TODO -> Arrumar as datas de acordo com o metodo obterData() que esta em PR [Apreciacao por dia];
		var data = {
			'data_inicio': "2022-01-06",
			'data_fim': "2022-01-06"
		}
		criarRankingPorPeriodo(data);		
	}
	
	function carregarRankingPeriodoDeDatas() {
		var filtroDataAdminViewModel = new FiltroDataAdminViewModel()
		ranking_colaboradores = criarRankingPorPeriodo(filtroDataAdminViewModel);
		ordenaRankingPorPilar();
	}

	function carregarRankingPilar() {
		var objetoClicado = $(this);

		$.getJSON("/reconhecimentos/ranking_de_pilares/" + objetoClicado.data('pilar_ranking-id') , function (ranking_de_colaboradores) {
			template.exibirEm('div[data-js="container__ranking"]', rankingAdmin ,ranking_de_colaboradores);
		});
	}

	function criarRankingPorPeriodo(dataAdminViewModel) {
		$.post("/reconhecimentos/ranking_por_periodo/", dataAdminViewModel , function (ranking_de_colaboradores) {
			ranking_colaboradores = ranking_colaboradores;
			exibirRanking(ranking_de_colaboradores);
		});
	}

	function exibirRanking(ranking_de_colaboradores){
		template.exibirEm('div[data-js="container__ranking"]', rankingAdmin ,data);
	}

	function ordenaRankingPorPilar(){
		var pilar_selecionado = $("input[name=filtro__pilares__ranking]:checked").val();
		var ranking_por_pilar = ranking_colaboradores;

		ranking_por_pilar.colaboradores.sort(function(colaborador1, colaborador2){
			return colaborador1.pilar_selecionado > colaborador2.pilar_selecionado;
		});
		
		template.exibirEm('div[data-js="container__ranking"]', rankingAdmin ,ranking_por_pilar);
	}

	return self;
});
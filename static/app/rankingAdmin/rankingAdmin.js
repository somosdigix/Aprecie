define([
	"jquery",
	"template",
	"text!app/rankingAdmin/rankingAdminTemplate.html",
	"text!app/rankingAdmin/ranking_sem_filtros.html",
	'app/models/filtroDataAdminViewModel'
], function ($, template, rankingAdminTemplate, ranking_sem_filtros, FiltroDataAdminViewModel) {
	"use strict";

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;

		$('#conteudo')
		.on('click', 'input[data-js="colaborarSempre"]', carregarRankingPilar)
		.on('click', 'input[data-js="focarNasPessoas"]', carregarRankingPilar)
		.on('click', 'input[data-js="fazerDiferente"]', carregarRankingPilar)
		.on('click', 'input[data-js="planejarEntregarAprender"]', carregarRankingPilar)
		.on('click', 'button[data-js="botao__ranking__adm"]', carregarRankingPeriodoDeDatas);

		carregarRankingAdmin();
	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};

	function carregarRankingAdmin() {
		$.getJSON("/reconhecimentos/ranking_de_pilares/1", function (ranking_de_colaboradores) {
			template.exibir(rankingAdminTemplate, ranking_de_colaboradores);
		});
	}
	
	function carregarRankingPeriodoDeDatas() {
		var filtroDataAdminViewModel = new FiltroDataAdminViewModel()

		$.getJSON("/reconhecimentos/ranking_por_periodo/", filtroDataAdminViewModel , function (ranking_de_colaboradores) {
			template.exibirEm('div[data-js="container__ranking"]', rankingAdminTemplate,ranking_de_colaboradores);
		});
	}

	function carregarRankingPilar() {
		var objetoClicado = $(this);

		$.getJSON("/reconhecimentos/ranking_de_pilares/" + objetoClicado.data('pilar_ranking-id') , function (ranking_de_colaboradores) {
			template.exibirEm('div[data-js="container__ranking"]', ranking_sem_filtros ,ranking_de_colaboradores);
		});
	}

	return self;
});
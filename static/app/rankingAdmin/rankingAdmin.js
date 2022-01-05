define([
	"jquery",
	"template",
	"text!app/rankingAdmin/rankingAdminTemplate.html",
	"text!app/rankingAdmin/rankingAdmin.html",
	'app/models/filtroDataAdminViewModel'
], function ($, template, rankingAdminTemplate, rankingAdmin, FiltroDataAdminViewModel) {
	"use strict";

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;

		$('#conteudo')
		.on('click', 'button[data-js="colaborarSempre"]', carregarRankingPilar)
		.on('click', 'button[data-js="focarNasPessoas"]', carregarRankingPilar)
		.on('click', 'button[data-js="fazerDiferente"]', carregarRankingPilar)
		.on('click', 'button[data-js="planejarEntregarAprender"]', carregarRankingPilar)
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

		$.post("/reconhecimentos/ranking_por_periodo/", filtroDataAdminViewModel , function (ranking_de_colaboradores) {
			template.exibirEm('div[data-js="container__ranking"]', rankingAdminTemplate,ranking_de_colaboradores);
		});
	}

	function carregarRankingPilar() {
		var objetoClicado = $(this);

		$.getJSON("/reconhecimentos/ranking_de_pilares/" + objetoClicado.data('pilar_ranking-id') , function (ranking_de_colaboradores) {
			template.exibirEm('div[data-js="container__ranking"]', rankingAdminTemplate ,ranking_de_colaboradores);
		});
	}

	return self;
});
define([
	"jquery",
	"template",
	"text!app/ranking/rankingTemplate.html",
	"text!app/ranking/rankingAdminTemplate.html",
], function ($, template, rankingTemplate, rankingAdminTempleate) {
	"use strict";

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;

		carregarRanking();
	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};

	function carregarRanking() {
		$.getJSON("/reconhecimentos/ranking", function (ranking_de_colaboradores) {
			template.exibir(rankingTemplate, ranking_de_colaboradores);
			imagemMedalhaDinamica();
		});
	}

	function carregarRankingPeriodoDeDatas() {
		$.getJSON("/reconhecimentos/ranking_por_periodo", function (ranking_de_colaboradores) {
			template.exibir(rankingAdminTempleate, ranking_de_colaboradores);
		});
	}

	function carregarRankingPilar(id_pilar) {
		$.getJSON("/reconhecimentos/ranking_de_pilar/" + id_pilar , function (ranking_de_colaboradores) {
			template.exibir(rankingAdminTempleate, ranking_de_colaboradores);
		});
	}

	return self;
});

function imagemMedalhaDinamica() {
	var imagem = document.getElementsByClassName("medalha");
	for (var i = 0; i < imagem.length; i++) {
		var img = document.createElement("img");
		img.src = "../static/img/medalhas/medalha" + i + ".svg";
		img.id = "posicao";
		var medalha = imagem[i];
		console.log(medalha);
		medalha.appendChild(img);
	}
}

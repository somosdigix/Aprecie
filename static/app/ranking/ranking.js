define([
	"jquery",
	"template",
	"text!app/ranking/rankingTemplate.html"
], function ($, template, rankingTemplate) {
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

	return self;
});

function imagemMedalhaDinamica() {
	var imagem = document.getElementsByClassName("medalha");
	for (var i = 0; i < imagem.length; i++) {
		var img = document.createElement("img");
		img.src = "../static/img/medalhas/medalha" + i + ".svg";
		img.className = "posicao__medalha"
		img.id = "posicao" + i;
		var medalha = imagem[i];
		medalha.appendChild(img);
	}
}

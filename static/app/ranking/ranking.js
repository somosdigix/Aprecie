define([
    'jquery',
	'template',
	'text!app/ranking/rankingTemplate.html',
], function($, template, rankingTemplate) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;
        
        carregarRanking()
	};

	self.finalizar = function() {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	function carregarRanking() {
		$.getJSON('/reconhecimentos/ranking', function(ranking_de_colaboradores){
            template.exibir(rankingTemplate, ranking_de_colaboradores);
        });
	}

	return self;
});
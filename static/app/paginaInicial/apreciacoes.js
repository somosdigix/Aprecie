define([
	'text!app/paginaInicial/ultimasApreciacoesTemplate.html',
	'text!app/paginaInicial/apreciacoesTemplate.html'
], function(ultimasApreciacoesTemplate, apreciacoesTemplate) {
	'use strict';

	var self = {};
	var _sandbox, _paginaAtual;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;
		_paginaAtual = 0;

		$('#conteudo').on('click', 'button[data-js="carregar-mais"]', carregarApreciacoes);

		_sandbox.acrescentarTemplateEm('#conteudo', ultimasApreciacoesTemplate);
		carregarApreciacoes();
	};

	self.finalizar = function() {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	function carregarApreciacoes() {
		_paginaAtual++;
		$('button[data-js="carregar-mais"]').attr('disabled', 'disabled');

		_sandbox.getJSON('/reconhecimentos/ultimos/', { pagina_atual: _paginaAtual }).then(exibirUltimasApreciacoes);
	}

	function exibirUltimasApreciacoes(ultimosReconhecimentos) {
		var totalDePaginas = ultimosReconhecimentos.total_de_paginas;
		var conteudo = _sandbox.compilarTemplate(apreciacoesTemplate, ultimosReconhecimentos);

		$('div[data-js="ultimas-apreciacoes"]').append(conteudo);

		if (totalDePaginas === _paginaAtual)
			$('button[data-js="carregar-mais"]').hide();
		else
			$('button[data-js="carregar-mais"]').removeAttr('disabled');
	}

	return self;
});
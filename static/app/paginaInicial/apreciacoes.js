define([
	'text!app/paginaInicial/apreciacoesTemplate.html'
], function(apreciacoesTemplate) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;

		_sandbox.getJSON('/reconhecimentos/ultimos/').then(exibirTemplate);
	};

	self.finalizar = function() {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	function exibirTemplate(ultimosReconhecimentos) {
		_sandbox.acrescentarTemplateEm('#conteudo', apreciacoesTemplate, ultimosReconhecimentos);
	}

	return self;
});
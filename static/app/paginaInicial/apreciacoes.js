define([
	'text!partials/apreciacoesTemplate.html'
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
		_sandbox.registrarEvento('click', '#conteudo', 'strong[data-js="ir-ao-perfil"]', irAoPerfil);
		// $('body').removeClass('body-login').addClass('body-app');
	}

	function irAoPerfil() {
		var id = _sandbox.data(this, 'id');
		_sandbox.navegarPara('/perfil/' + id);
	};

	return self;
});
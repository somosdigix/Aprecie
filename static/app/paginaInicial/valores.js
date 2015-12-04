define([
	'text!partials/valoresDaEmpresaTemplate.html'
],	function(valoresDaEmpresaTemplate) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;

		_sandbox.exibirTemplate('#conteudo', valoresDaEmpresaTemplate);
	};

	self.finalizar = function() {
		_sandbox.limpar('#conteudo');
	};

	return self;
});
define([
	'text!app/cadastroDeColaboradores/formularioTemplate.html'
], function(cadastroTemplate) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;

		_sandbox.exibirTemplateEm('#conteudo', cadastroTemplate);
	};

	self.finalizar = function() {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

    return self;
});
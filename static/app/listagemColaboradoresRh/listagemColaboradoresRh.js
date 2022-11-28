define([
	"jquery",
	'text!app/listagemColaboradoresRh/listagemColaboradoresRh.html',
], function ($, template) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;
		_sandbox.exibirTemplateEm('#conteudo', template);
	};

	self.finalizar = function () {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	return self;
});
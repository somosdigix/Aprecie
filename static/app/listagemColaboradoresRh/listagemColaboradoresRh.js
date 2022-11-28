define([
	"jquery",
	'text!app/listagemColaboradoresRh/listagemColaboradoresRh.html',
], function ($, template) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;
		
		$.getJSON("/login/listagemColaboradoresRh", function (colaboradores) {
			_sandbox.exibirTemplateEm('#conteudo', template, colaboradores);
		})
	};

	self.finalizar = function () {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	return self;
});
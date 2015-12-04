define([
	'gerenciadorDeModulos',
	'app/login/logon',
	'app/login/autenticacao'
], function(gerenciadorDeModulos, logon, autenticacao) {
	'use strict';

	var self = {};

	self.exibir = function() {
		gerenciadorDeModulos.registrar('logon', logon);
		gerenciadorDeModulos.registrar('autenticacao', autenticacao);

		gerenciadorDeModulos.iniciarTodos();
	};

	self.finalizar = function() {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return self;
});
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
		// TODO: Unificar se for igual a todos os controllers
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return self;
});
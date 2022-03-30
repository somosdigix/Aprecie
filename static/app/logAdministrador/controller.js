define([
	'gerenciadorDeModulos',
	'app/logAdministrador/logAdministrador'
], function(gerenciadorDeModulos, logAdministrador) {
	'use strict';

	var _self = {};

	_self.exibir = function() {
		gerenciadorDeModulos.registrar('logAdministrador', logAdministrador);
		gerenciadorDeModulos.iniciarTodos();
	};

	_self.finalizar = function() {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
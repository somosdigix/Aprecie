define([
	'gerenciadorDeModulos',
	'app/rankingAdmin/rankingAdmin'
], function(gerenciadorDeModulos, rankingAdmin) {
	'use strict';

	var _self = {};

	_self.exibir = function() {
		gerenciadorDeModulos.registrar('rankingAdmin', rankingAdmin);
		gerenciadorDeModulos.iniciarTodos();
	};

	_self.finalizar = function() {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
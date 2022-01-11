define([
	'gerenciadorDeModulos',
	'app/ranking/ranking'
], function(gerenciadorDeModulos, ranking) {
	'use strict';

	var _self = {};

	_self.exibir = function() {
		gerenciadorDeModulos.registrar('ranking', ranking);
		gerenciadorDeModulos.iniciarTodos();
	};

	_self.finalizar = function() {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
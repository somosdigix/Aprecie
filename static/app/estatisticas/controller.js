define([
	'gerenciadorDeModulos',
	'app/estatisticas/estatisticas'
], function(gerenciadorDeModulos, estatisticas) {
	'use strict';

	var _self = {};

	_self.exibir = function() {
		gerenciadorDeModulos.registrar('estatisticas', estatisticas);
		gerenciadorDeModulos.iniciarTodos();
	};

	_self.finalizar = function() {
		// TODO: Unificar se for igual a todos os controllers
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
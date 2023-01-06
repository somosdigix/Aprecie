define([
	'gerenciadorDeModulos',
	'app/cadastroDeColaboradores/cadastroDeColaboradores'
], function(gerenciadorDeModulos, cadastroDeColaboradores) {
	'use strict';

	var _self = {};

	_self.exibir = function(colaboradorId) {
		gerenciadorDeModulos.registrar('cadastroDeColaboradores', cadastroDeColaboradores);
		gerenciadorDeModulos.iniciarTodos(colaboradorId);
	};

	_self.finalizar = function() {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
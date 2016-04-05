define([
	'gerenciadorDeModulos',
	'app/reconhecimentos/reconhecer',
	'app/reconhecimentos/reconhecimentos'
], function(gerenciadorDeModulos, reconhecer, reconhecimentos) {
	'use strict';

	var _self = {};

	_self.exibir = function(colaboradorId, valorId) {
		gerenciadorDeModulos.registrar('reconhecimentos', reconhecimentos);
		gerenciadorDeModulos.iniciarTodos(colaboradorId, valorId);
	};

	_self.finalizar = function() {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
})
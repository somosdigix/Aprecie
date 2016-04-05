define([
	'gerenciadorDeModulos',
	'app/paginaInicial/apreciacoes'
], function(gerenciadorDeModulos, apreciacoes) {
	'use strict';

	var _self = {};

	_self.exibir = function() {
		gerenciadorDeModulos.registrar('apreciacoes', apreciacoes);
		gerenciadorDeModulos.iniciarTodos();
	};

	_self.finalizar = function() {
		// TODO: Unificar se for igual a todos os controllers
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
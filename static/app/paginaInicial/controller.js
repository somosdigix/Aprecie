define([
	'gerenciadorDeModulos',
	'app/paginaInicial/valores',
	'app/paginaInicial/apreciacoes'
], function(gerenciadorDeModulos, valores, apreciacoes) {
	'use strict';

	var self = {};

	self.exibir = function() {
		gerenciadorDeModulos.registrar('valores', valores);
		gerenciadorDeModulos.registrar('apreciacoes', apreciacoes);

		gerenciadorDeModulos.iniciarTodos();
	};

	self.finalizar = function() {
		// TODO: Unificar se for igual a todos os controllers
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return self;
});
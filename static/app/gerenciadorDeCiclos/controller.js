define([
	'gerenciadorDeModulos',
	'app/gerenciadorDeCiclos/gerenciadorDeCiclos'
], function(gerenciadorDeModulos, gerenciadorDeCiclos) {
	'use strict';

	var _self = {};

	_self.exibir = function() {
		gerenciadorDeModulos.registrar('gerenciadorDeCiclos', gerenciadorDeCiclos);
		gerenciadorDeModulos.iniciarTodos();
	};

	_self.finalizar = function() {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
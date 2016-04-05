define([
	'gerenciadorDeModulos',
	'app/perfil/perfil'
], function(gerenciadorDeModulos, perfil) {
	'use strict';

	var _self = {};

	_self.exibir = function(colaboradorId) {
		gerenciadorDeModulos.registrar('perfil', perfil);
		gerenciadorDeModulos.iniciarTodos(colaboradorId);
	};

	_self.finalizar = function() {
		// TODO: Unificar isso, repete em todos os controllers
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
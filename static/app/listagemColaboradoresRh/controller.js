define([
	'gerenciadorDeModulos',
	'app/listagemColaboradoresRh/listagemColaboradoresRh'
], function (gerenciadorDeModulos, listagemColaboradoresRh) {
	'use strict';

	var _self = {};

	_self.exibir = function () {
		gerenciadorDeModulos.registrar('listagemColaboradoresRh', listagemColaboradoresRh);
		gerenciadorDeModulos.iniciarTodos();
	};

	_self.finalizar = function () {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});
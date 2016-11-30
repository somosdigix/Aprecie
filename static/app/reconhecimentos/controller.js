define([
	'gerenciadorDeModulos',
  'app/perfil/apreciar',
	'app/reconhecimentos/reconhecimentos',
], function(gerenciadorDeModulos, apreciar, reconhecimentos) {
	'use strict';

	var _self = {};

	_self.exibir = function(colaboradorId, valorId) {
    gerenciadorDeModulos.registrar('apreciar', apreciar);
		gerenciadorDeModulos.registrar('reconhecimentos', reconhecimentos);
		gerenciadorDeModulos.iniciarTodos(colaboradorId, valorId);
	};

	_self.finalizar = function() {
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
})
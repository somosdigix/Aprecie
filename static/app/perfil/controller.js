define([
	'gerenciadorDeModulos',
  'app/perfil/perfil',
	'app/perfil/reconhecimentosHistoricos',
], function(gerenciadorDeModulos, perfil, reconhecimentosHistoricos) {
	'use strict';

	var _self = {};

	_self.exibir = function(colaboradorId) {
    gerenciadorDeModulos.registrar('perfil', perfil);
		gerenciadorDeModulos.registrar('reconhecimentosHistoricos', reconhecimentosHistoricos);
		gerenciadorDeModulos.iniciarTodos(colaboradorId);
	};

	_self.finalizar = function() {
		// TODO: Unificar isso, repete em todos os controllers
		gerenciadorDeModulos.finalizarTodos();
		gerenciadorDeModulos.removerTodos();
	};

	return _self;
});

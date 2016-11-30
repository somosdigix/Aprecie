define([
	'gerenciadorDeModulos',
  'app/perfil/perfil',
  'app/perfil/apreciar',
	'app/perfil/reconhecimentosHistoricos',
], function(gerenciadorDeModulos, perfil, apreciar, reconhecimentosHistoricos) {
	'use strict';

	var _self = {};

	_self.exibir = function(colaboradorId) {
    gerenciadorDeModulos.registrar('perfil', perfil);
    gerenciadorDeModulos.registrar('apreciar', apreciar);
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

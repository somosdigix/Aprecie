define([
	'sandbox'
], function(Sandbox) {
	'use strict';
	
	var self = {};
	var _modulos = {};
	var _eventos = {};

	self.registrar = function(moduloId, modulo) {
		_modulos[moduloId] = modulo;
	};

	self.iniciar = function(moduloId, parametrosAdicionais) {
		var sandbox = new Sandbox(this);
		var parametros = parametrosAdicionais.slice(0);
		parametros.unshift(sandbox);

		_modulos[moduloId].inicializar.apply(this, parametros);
	};

	self.finalizar = function(moduloId) {
		var modulo = _modulos[moduloId];

		if (modulo.finalizar)
			modulo.finalizar();
	};

	self.remover = function(moduloId) {
		if (_modulos[moduloId])
			delete _modulos[moduloId];
	};

	self.iniciarTodos = function() {
		var parametrosAdicionais = Array.prototype.slice.call(arguments);

		for (var moduloId in _modulos)
			self.iniciar(moduloId, parametrosAdicionais);
	};

	self.finalizarTodos = function() {
		for (var moduloId in _modulos)
			self.finalizar(moduloId);
	};

	self.removerTodos = function() {
		for (var moduloId in _modulos)
			self.remover(moduloId);
	};

	self.escutar = function(nomeDoEvento, callback) {
		if (_eventos[nomeDoEvento])
			throw new Error('Nome de evento já registrado');

		_eventos[nomeDoEvento] = callback;
	};

	self.removerEscuta = function(nomeDoEvento) {
		var evento = _eventos[nomeDoEvento];

		if (evento)
			delete _eventos[nomeDoEvento];
	};

	self.notificar = function(nomeDoEvento, dados) {
    	var parametros = Array.prototype.slice.call(arguments);
		var nomeDoEvento = parametros[0];
		var dados = parametros.slice(1);

		if (!_eventos[nomeDoEvento]) return;

		_eventos[nomeDoEvento].apply(this, dados);
	};

	return self;
});
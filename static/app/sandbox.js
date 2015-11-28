define([
	'jquery',
	'app/helpers/ajax',
	'roteador',
	'configuracoes',
	'sessaoDeUsuario',
	'app/servicos/servicoDeAutenticacao',
	'template'
], function($, ajax, roteador, configuracoes, sessaoDeUsuario, servicoDeAutenticacao, template) {
	'use strict';

	function Sandbox(gerenciadorDeModulos) {
		var self = this;
		var eventos = {};
		var _gerenciadorDeModulos = gerenciadorDeModulos;

		self.ehDebug = function() {
			return configuracoes.ehDebug();
		};

		self.navegarPara = function(endereco) {
			roteador.navegarPara(endereco);
		};

		self.exibirTemplate = function(container, nomeDoTemplate, dados) {
			return template.exibirComRequire(container, nomeDoTemplate, dados);
		};

		self.limpar = function(seletor) {
			$(seletor).empty();
		};

		self.escutar = function(nomeDoEvento, callback) {
			_gerenciadorDeModulos.escutar(nomeDoEvento, callback);
		};

		self.removerEscuta = function(nomeDoEvento) {
			_gerenciadorDeModulos.removerEscuta(nomeDoEvento);
		};

		self.notificar = function(nomeDoEvento, callback) {
			_gerenciadorDeModulos.notificar.apply(this, arguments);
		};

		self.post = function(url, dados) {
			return ajax.post(url, dados);
		};

		self.registrarEvento = function(evento, container, alvo, callback) {
			$(container).on(evento, alvo, callback);
		};

		self.removerEvento = function(container) {
			$(container).off();
		};

		self.alterarTexto = function(seletor, novoTexto) {
			$(seletor).text(novoTexto);
		};

		self.preencherSessao = function(colaborador) {
			sessaoDeUsuario.preencherDados(colaborador);
		};

		self.preencherCookie = function(colaborador) {
			servicoDeAutenticacao.autenticar(colaborador);
		};
	}

	return Sandbox;
});
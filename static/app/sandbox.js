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

		self.exibirTemplate = function(conteudo, modelo) {
			template.exibir(conteudo, modelo);
		};

		self.exibirTemplateEm = function(container, conteudo, modelo) {
			template.exibirEm(container, conteudo, modelo);
		};

		self.acrescentarTemplateEm = function(container, conteudo, modelo) {
			template.acrescentarEm(container, conteudo, modelo);
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

		self.getJSON = function(url, parametros) {
			return ajax.getJSON(url, parametros);
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

		self.data = function(seletor, nomeDoAtributo) {
			return $(seletor).data(nomeDoAtributo)
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
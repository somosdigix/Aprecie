define([
	'jquery',
	'app/helpers/ajax',
	'roteador',
	'configuracoes'
], function($, ajax, roteador, configuracoes) {
	'use strict';

	function Sandbox(controlador) {
		var self = this;
		var eventos = {};
		var _controlador = controlador;

		self.ehDebug = function() {
			return configuracoes.ehDebug();
		};

		self.navegarPara = function(endereco) {
			roteador.navegarPara(endereco);
		};

		self.exibirTemplate = function(container, nomeDoTemplate, dados) {
			var acao = function(resolver) {
				var urlDoTemplate = 'text!partials/' + nomeDoTemplate;

				require([
					urlDoTemplate,
					'handlebars'
				], function(template, Handlebars) {
					var jContainer = $(container);
					var conteudo = Handlebars.compile(template)(dados);

					jContainer.append(conteudo);
					resolver();
				});
			};

			return new Promise(acao);
		};

		self.escutar = function(nomeDoEvento, callback) {
			_controlador.escutar(nomeDoEvento, callback);
		};

		self.notificar = function(nomeDoEvento, callback) {
			_controlador.notificar.apply(this, arguments);
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
	}

	return Sandbox;
});
define([
	"jquery",
	"template",
    "text!app/logAdministrador/logAdministradorTemplate.html",
    "text!app/logAdministrador/administradoresTemplate.html",
    "text!app/logAdministrador/historicoAdministradorTemplate.html",
], function ($, template, logAdministradorTemplate, administradoresTemplate, historicoAdministradorTemplate) {
	"use strict";

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;
        
        template.exibir(logAdministradorTemplate);
        carregarColaboradoresAdministradores();
        carregarHistoricoAlteracaoAdministradores();
	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};

    function carregarColaboradoresAdministradores() {
		template.exibirEm('div[data-js="container-colaboradores-administradores"]', administradoresTemplate);
	}

    function carregarHistoricoAlteracaoAdministradores() {
		template.exibirEm('div[data-js="container-historico-alteracao-administrador"]', historicoAdministradorTemplate);
	}

	return self;
});
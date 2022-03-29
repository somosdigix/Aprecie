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

		$('#conteudo').on('click', 'button[data-js="botao__log_administrador"]', carregarHistoricoAlteracaoAdministradores);
	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};

    function carregarColaboradoresAdministradores() {
		$.getJSON("/login/obter_administradores", function (administradores) {
			template.exibirEm('div[data-js="container-colaboradores-administradores"]', administradoresTemplate, administradores);
        });
	}

    function carregarHistoricoAlteracaoAdministradores() {
		var data = {
			'data_inicio': $('#data_inicio').val(),
			'data_fim': $('#data_fim').val(),
		}

		$.post("/login/obter_logs_administradores/", data, function (historico_logs_administrador) {
			template.exibirEm('div[data-js="container-historico-alteracao-administrador"]', historicoAdministradorTemplate, historico_logs_administrador);
        });
	}

	return self;
});
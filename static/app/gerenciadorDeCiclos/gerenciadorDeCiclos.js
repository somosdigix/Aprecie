define([
	"jquery",
	"template",
	"text!app/gerenciadorDeCiclos/gerenciadorDeCiclosTemplate.html",
    "sessaoDeUsuario",
], function ($, template, gerenciadorDeCiclosTemplate, sessaoDeUsuario) {
	"use strict";

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;
        carregarGerenciador()

        // on click button html para função de definir ciclo e alterar ciclo
	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};

    function carregarGerenciador(){
        $.getJSON("/reconhecimentos/obterCiclos", function (ciclos) {
			template.exibir(gerenciadorDeCiclosTemplate, ciclos);
		});
    }
	
    // alteracao e definicao de ciclo fazer funcoes
    function definirCiclo(){
        data = {
            'data_inicial': $('.data_inicial_ciclo').val(),
            'data_final': $('.data_final_ciclo').val(),
            'usuario_que_modificou': sessaoDeUsuario.id
        }
        
        $.post('/reconhecimentos/definir_ciclo/', data, function () {
			growl.deSucesso().exibir('Ciclo adicionado com sucesso');
			roteador.atualizar();
		})
    }

    function alterarCiclo(){
        data = {
            'id_ciclo': $('.id_ciclo').val(),
            'data_inicial': $('.data_inicial_ciclo').val(),
            'data_final': $('.data_final_ciclo').val(),
            'usuario_que_modificou': sessaoDeUsuario.id ,
            'descricao_da_alteracao': $('.descricao_da_alteracao').val()
        }

        $.post('/reconhecimentos/alterar_ciclo/', data, function () {
			growl.deSucesso().exibir('Ciclo alterado com sucesso');
			roteador.atualizar();
		})
    }


	return self;
});
define([
	"jquery",
	"template",
	"text!app/gerenciadorDeCiclos/gerenciadorDeCiclosTemplate.html",
    "sessaoDeUsuario",
    "growl",
    "roteador"
], function ($, template, gerenciadorDeCiclosTemplate, sessaoDeUsuario, growl,  roteador) {
	"use strict";

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;
        carregarGerenciador()

        // on click button html para função de definir ciclo e alterar ciclo
        $("#conteudo")
            .on("click", 'button[data-js="btn_adicionar_ciclo"]', definirCiclo)
			.on("click", 'button[data-js="btn_alterar_ciclo"]', alterarCiclo)
	};

	self.finalizar = function () {
		_sandbox.limpar("#conteudo");
		_sandbox.removerEvento("#conteudo");
	};

    function carregarGerenciador(){
        $.getJSON("/reconhecimentos/obter_informacoes_ciclo_atual", function (ciclo_atual) {
			template.exibir(gerenciadorDeCiclosTemplate, ciclo_atual);
		});
    }
	
    function definirCiclo(){       
        var data = {
            'nome_ciclo': $('#nome_ciclo').val(),
            'data_inicial': $('#data_inicial').val(),
            'data_final': $('#data_final').val(),
            'usuario_que_modificou': sessaoDeUsuario.id
        }
        
        $.post('/reconhecimentos/definir_ciclo/', data, function () {
			growl.deSucesso().exibir('Ciclo adicionado com sucesso');
			roteador.atualizar();
		})
    }

    function alterarCiclo(){
        var data = {
            'id_ciclo': $('#id_ciclo').val(),
            'data_final': $('#nova__data__final').val(),
            'usuario_que_modificou': sessaoDeUsuario.id ,
            'descricao_da_alteracao': $('#input__motivo').val()
        }

        $.post('/reconhecimentos/alterar_ciclo/', data, function () {
			growl.deSucesso().exibir('Ciclo alterado com sucesso');
			roteador.atualizar();
		})
    }


	return self;
});
define([
    "jquery",
    "template",
    "text!app/gerenciadorDeCiclos/gerenciadorDeCiclosTemplate.html",
    "text!app/gerenciadorDeCiclos/ciclosPassadosTemplate.html",
    "sessaoDeUsuario",
    "growl",
    "roteador"
], function ($, template, gerenciadorDeCiclosTemplate, ciclosPassadosTemplate, sessaoDeUsuario, growl, roteador) {
    "use strict";

    var self = {};
    var _sandbox;

    self.inicializar = function (sandbox) {
        _sandbox = sandbox;

        carregarGerenciador();

        // on click button html para função de definir ciclo e alterar ciclo
        $("#conteudo")
            .on("click", 'button[data-js="btn_adicionar_ciclo"]', definirCiclo)
            .on("click", 'button[data-js="btn_alterar_ciclo"]', alterarCiclo)
    };

    self.finalizar = function () {
        _sandbox.limpar("#conteudo");
        _sandbox.removerEvento("#conteudo");
    };

    async function carregarGerenciador() {
        await $.getJSON("/reconhecimentos/obter_informacoes_ciclo_atual", function (ciclo_atual) {
            template.exibir(gerenciadorDeCiclosTemplate, ciclo_atual);
        });

        await carregarCiclosPassados();

        definirPorcentagemNoCirculo();
    }

    async function definirPorcentagemNoCirculo() {
        var porcentagem = await $('#porcentagem').html();
        await $("#circulo2").css("stroke-dashoffset", 314 - (parseInt(porcentagem) / 100) * 314);
    }

    async function carregarCiclosPassados() {
        await $.getJSON("/reconhecimentos/ciclos_passados", function (ciclos_passados) {
            template.acrescentarEm('#corpo__historico', ciclosPassadosTemplate, ciclos_passados);
        });

        await $("#secao1").toggleClass('secaoSelecionada');
        $("#1").prop("checked", true);
    }

    //funcoes para editar ciclo
    function definirCiclo() {
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

    function alterarCiclo() {
        var data = {
            'id_ciclo': $('#id_ciclo').val(),
            'data_final': $('#nova__data__final').val(),
            'usuario_que_modificou': sessaoDeUsuario.id,
            'descricao_da_alteracao': $('#input__motivo').val()
        }

        $.post('/reconhecimentos/alterar_ciclo/', data, function () {
            growl.deSucesso().exibir('Ciclo alterado com sucesso');
            roteador.atualizar();
        })
    }

    //funcoes para abrir e fechar modal
    function mostrarContainerNovoCiclo() {
        document.getElementById("container__novo__ciclo").style.display = "block";
    }
    function fecharContainerNovoCiclo() {
        document.getElementById("container__novo__ciclo").style.display = "none";
    }
    function fecharModal() {
        document.getElementById("abrirModal").style.opacity = "0";
        document.getElementById("abrirModal").style.pointerEvents = "none";
    }
    function mostrarModal() {
        document.getElementById("abrirModal").style.opacity = "1";
        document.getElementById("abrirModal").style.pointerEvents = "auto";
    }

    return self;
});
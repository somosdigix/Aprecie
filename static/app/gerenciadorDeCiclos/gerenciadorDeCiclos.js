define([
    "jquery",
    "template",
    "text!app/gerenciadorDeCiclos/gerenciadorDeCiclosTemplate.html",
    "text!app/gerenciadorDeCiclos/ciclosPassadosTemplate.html",
    "text!app/gerenciadorDeCiclos/historicoDeAlteracao.html",
    "sessaoDeUsuario",
    "growl",
    "roteador"
], function ($, template, gerenciadorDeCiclosTemplate, ciclosPassadosTemplate,historicoDeAlteracao,sessaoDeUsuario, growl, roteador) {
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
            .on("click", 'button[id="btn__editar"]', mostrarModal)
            .on("click", 'button[id="btn__cancelar__edicao"]', fecharModal)
            .on("click", 'button[id="btn__adicionar__ciclo"]',mostrarContainerNovoCiclo)
            .on("click", 'button[id="btn__cancelar"]',fecharContainerNovoCiclo)
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

        await carregarHistoricoAlteracoes();

        $('#corpo__historico').hide();
        $('#historico_alteracao').hide();

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

        await $("div.opcaoSecao--ciclos#secaoc1").toggleClass('secaoSelecionada');
        await $("input.para__ciclos#c1").prop("checked", true);
    }
    
    async function carregarHistoricoAlteracoes() {
        await $.getJSON("/reconhecimentos/historico_alteracoes", function (LOG_ciclos) {
            template.acrescentarEm('#historico_alteracao', historicoDeAlteracao, LOG_ciclos);
        });

        await $("div.opcaoSecao--historico#secaoh1").toggleClass('secaoSelecionada');
        await $("input.para__historico#h1").prop("checked", true);
    }

    //funcoes para editar ciclo
    function definirCiclo(event) {
        event.preventDefault();
        var data = {
            'nome_ciclo': $('#nome_ciclo').val(),
            'data_inicial': $('#data_inicial').val(),
            'data_final': $('#data_final').val(),
            'usuario_que_modificou': sessaoDeUsuario.id
        }
        var dataAtual = new Date();
        var dataInicial = new Date(data.data_inicial);
        var dataFinal = new Date(data.data_final);
        
        if(validacaoDataInicialMenor(dataInicial, dataAtual)) return;
        if(validacaoDataFinalMenor(dataInicial, dataFinal)) return;
        adicionarNoBanco(data);


    }

    function alterarCiclo(event) {
        event.preventDefault();
        var data = {
            'id_ciclo': $('#id_ciclo').val(),
            'data_inicial': $("#dataTeste").attr("value"),
            'data_final': $('#nova__data__final').val(),
            'usuario_que_modificou': sessaoDeUsuario.id,
            'descricao_da_alteracao': $('#input__motivo').val(),
            'novo_nome_ciclo': $('#novo_nome_ciclo').val()
        }
        var dataAtual = new Date();
        var dataFinal = new Date(data.data_final);
        var dataInicial = new Date(data.data_inicial);
        console.log(dataInicial);
        console.log(dataFinal)
        if(validacaoDataFinalMenorAlterada(dataFinal, dataInicial)) return;
        if(validacaoDataFinalAlteradaMenorDataAtual(dataFinal, dataAtual)) return;
        console.log("entrou no banco")
        alterarNoBanco(data);
        
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

    function exibirErroDaDiv(nomeErro){
        $(nomeErro).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
    }

    function validacaoDataInicialMenor(dataInicial, dataAtual){
        if(dataInicial < dataAtual){ 
            exibirErroDaDiv('.falha-data-inicial-menor');
            return true;
        }
        return false;
    }
    function validacaoDataFinalMenor(dataInicial, dataFinal){
        if(dataFinal < dataInicial){
            exibirErroDaDiv('.falha-data-final-menor');
            return true;
        }
        return false;
    }
    function validacaoDataFinalMenorAlterada(dataFinal, dataInicial){
        if(dataFinal < dataInicial){
            exibirErroDaDiv('.falha-data-final-menor-alterada');
            return true;
        }
        return false;
    }
    function validacaoDataFinalAlteradaMenorDataAtual(dataFinal, dataAtual){
        if(dataFinal < dataAtual){
            exibirErroDaDiv('.falha-data-final-menor-atual');
            return true;
        }
        return false;
    }
    function adicionarNoBanco(data){
        $.post('/reconhecimentos/definir_ciclo/', data, function () {
        growl.deSucesso().exibir('Ciclo adicionado com sucesso');
        roteador.atualizar();
      })};

    function alterarNoBanco(data){
        $.post('/reconhecimentos/alterar_ciclo/',data, function () {
            growl.deSucesso().exibir('Ciclo alterado com sucesso');
            roteador.atualizar();
    })};  
    return self;
});
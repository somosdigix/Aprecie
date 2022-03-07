
function exibirCiclos(seta) {
    var paiDaSeta = seta.parentElement;
    var idIrmaoDoPai = $(paiDaSeta).siblings('.container__historico').attr('id');

    if (seta.getAttribute('id') == 'setaAtivada') {
        seta.style.animation = "girarSetaCima 0.4s forwards";
        seta.setAttribute('id', 'setaDesativada');

        $(`#${idIrmaoDoPai}`).hide();
    }
    else {
        seta.setAttribute('id', 'setaAtivada');
        seta.style.animation = "girarSetaBaixo 0.4s forwards";
        $(`#${idIrmaoDoPai}`).show();
    }
}

//funcao usada pelas opcoes
function exibeCiclosCarrosel(numeroSecao, nome) {
    //a opcao que for marcada deve dizer de qual secao o carrosel deve prosseguir ou voltar
    $(`div.secaoSelecionada.${nome}`).toggleClass("secaoSelecionada");

    $(`div.${nome}#secao${numeroSecao}`).toggleClass("secaoSelecionada");
}

//funcao usada pela seta da direita
function mudarCiclosPelaSetaDireita(nome) {
    var idSecaoAtual = $(`input[name='${nome}']:checked`).attr('id');
    idSecaoDestino = transformarId(idSecaoAtual, 1);
    $('#' + idSecaoDestino).click();
}

//funcao usada pela seta da esquerda
function mudarCiclosPelaSetaEsquerda(nome) {
    var idSecaoAtual = $(`input[name='${nome}']:checked`).attr('id');
    idSecaoDestino = transformarId(idSecaoAtual, -1);
    $('#' + idSecaoDestino).click();
}

function exibirCiclosPeloTitulo(idTitulo) {
    var tituloJquery = $(`#${idTitulo}`);
    var setaIrma = $(tituloJquery).siblings('.seta__historico');

    setaIrma.click();
}
function transformarId(idSecaoAtual, exp){
    var idSecaoAtualArray = idSecaoAtual.toString().split('');
    idSecaoAtualArray[1] = parseInt(idSecaoAtualArray[1]) + exp;
    return idSecaoAtualArray.join('');
}
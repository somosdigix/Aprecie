define([
  'template',
  'text!app/perfil/apreciacoesRecebidasTemplate.html',
  'text!app/perfil/apreciacoesFeitasTemplate.html',
  'sessaoDeUsuario',
], function(template, apreciacoesRecebidasTemplate, apreciacoesFeitasTemplate, sessaoDeUsario) {
  'use strict';

  var _self = {};
  var _sandbox, _colaboradorId;
  var apreciacoesGlobal = {}

  _self.inicializar = function(sandbox, colaboradorId) {
    _sandbox = sandbox;
    _colaboradorId = colaboradorId;
    _sandbox.escutar('exibir-apreciacoes', obterApreciacoes);

    $('#conteudo')
        .on('click', 'button[data-js="reconhecimentos-feitos"]', exibirApreciacoesFeitas)
        .on('click', 'button[data-js="reconhecimentos-recebidos"]', exibirApreciacoesRecebidas);

  };

  _self.finalizar = function() {
    _sandbox.removerEscuta('exibir-apreciacoes');
  };

  function obterApreciacoes(){
    $.getJSON('/reconhecimentos/todos/' + _colaboradorId, function(apreciacoes) {
      apreciacoesGlobal = apreciacoes;
      exibirApreciacoesRecebidas();
    })
  }

  function exibirApreciacoesRecebidas() {
      template.exibirEm('div[data-js="todas-as-apreciacoes"]', apreciacoesRecebidasTemplate, apreciacoesGlobal.recebidas);

      if (sessaoDeUsario.id !== _colaboradorId){
        $("#reconhecimentos-recebidos").hide();
        $("#reconhecimentos-feitos").hide();

        var usuario = document.getElementsByName("compartilhar");
				for (var i = 0; i < usuario.length; i++){
					usuario[i].style.visibility = "hidden";
        }
      }
      else{
        document.querySelectorAll(".botao-agradecer").forEach( botao => {
          botao.style.display = "flex";
        })
      }
      
      $("#reconhecimentos-feitos").removeClass('botao__selecionado__perfil');
      $("#reconhecimentos-recebidos").addClass('botao__selecionado__perfil');
  }

  function exibirApreciacoesFeitas() {
    template.exibirEm('div[data-js="todas-as-apreciacoes"]', apreciacoesFeitasTemplate, apreciacoesGlobal.feitas);
    console.log(apreciacoesGlobal.feitas)
    $("#reconhecimentos-recebidos").removeClass('botao__selecionado__perfil');
    $("#reconhecimentos-feitos").addClass('botao__selecionado__perfil');
  }

  return _self;
});
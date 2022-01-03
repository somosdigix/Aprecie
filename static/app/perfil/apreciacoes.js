define([
  'template',
  'text!app/perfil/apreciacoesTemplate.html',
  'sessaoDeUsuario',
], function(template, apreciacoesTemplate, sessaoDeUsario) {
  'use strict';

  var _self = {};
  var _sandbox, _colaboradorId;

  _self.inicializar = function(sandbox, colaboradorId) {
    _sandbox = sandbox;
    _colaboradorId = colaboradorId;
    _sandbox.escutar('exibir-apreciacoes', exibirTodasAsApreciacoes);
  };

  _self.finalizar = function() {
    _sandbox.removerEscuta('exibir-apreciacoes');
  };

  function exibirTodasAsApreciacoes() {
    $.getJSON('/reconhecimentos/todos/' + _colaboradorId, function(apreciacoes) {
      template.exibirEm('div[data-js="todas-as-apreciacoes"]', apreciacoesTemplate, apreciacoes);
      if (sessaoDeUsario.id !== _colaboradorId){
        var usuario = document.getElementsByName("compartilhar");
				for (var i = 0; i < usuario.length; i++){
					usuario[i].style.visibility = "hidden";
        }
      }
    });
  }

  return _self;
});
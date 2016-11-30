define([
  'template',
  'text!app/perfil/apreciacoesTemplate.html',
], function(template, apreciacoesTemplate) {
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
    });
  }

  return _self;
});
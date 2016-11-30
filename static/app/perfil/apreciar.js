define([
], function() {
  'use strict';

  var _self = {};
  var _sandbox;

  _self.inicializar = function(sandbox) {
    _sandbox = sandbox;

    $('#conteudo')
      .on('click', 'div.escrever-apreciacao div.campos', selecionarPilar);
  };

  _self.finalizar = function() {
  };

  function selecionarPilar() {
    $('div.campos.selecionado').removeClass('selecionado');
    $(this).toggleClass('selecionado').find(':radio').attr('checked', true);
  }

  return _self;
});
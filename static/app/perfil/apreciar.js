define([
  'app/models/reconhecerViewModel',
  'growl',
  'roteador',
  'sessaoDeUsuario',
], function(ReconhecerViewModel, growl, roteador, sessaoDeUsuario) {
  'use strict';

  var _self = {};
  var _sandbox;

  _self.inicializar = function(sandbox, colaboradorId) {
    _sandbox = sandbox;

    $('#conteudo')
      .on('click', 'div.escrever-apreciacao div.campos', selecionarPilar)
      .on('click', 'button[data-js="reconhecer"]', reconhecer);
  };

  _self.finalizar = function() {
  };

  function selecionarPilar() {
    $('div.campos.selecionado').removeClass('selecionado');
    $(this).toggleClass('selecionado').find(':radio').attr('checked', true);
  }

  function reconhecer() {
    var reconhecerViewModel = new ReconhecerViewModel();
    validarOperacao(reconhecerViewModel);

    $.post('/reconhecimentos/reconhecer/', reconhecerViewModel, function() {
      growl.deSucesso().exibir('Reconhecimento realizado com sucesso');
      roteador.atualizar();
    });
  }

  function validarOperacao(reconhecerViewModel) {
    if (reconhecerViewModel.situacao === '')
      throw new ViolacaoDeRegra('A situação deve ser informada');

    if (reconhecerViewModel.comportamento === '')
      throw new ViolacaoDeRegra('O comportamento que a pessoa exibiu deve ser informado');

    if (reconhecerViewModel.impacto === '')
      throw new ViolacaoDeRegra('O impacto que isso gerou deve ser informado');
  }

  return _self;
});
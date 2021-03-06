﻿define([
  'jquery',
  'template',
  'text!app/perfil/perfilTemplate.html',
  'sessaoDeUsuario',
  'app/helpers/iconesDosValoresHelpers'
], function($, template, perfilTemplate, sessaoDeUsuario) {
  'use strict';

  var _self = {};
  var _sandbox;

  _self.inicializar = function(sandbox, colaboradorId) {
    _sandbox = sandbox;

    $.getJSON('/reconhecimentos/colaborador/' + colaboradorId, function(reconhecimentosDoColaborador) {
      template.exibir(perfilTemplate, reconhecimentosDoColaborador);

      $('#conteudo')
        .on('click', 'div[data-js="exibir-reconhecimentos"]', exibirReconhecimentos);

      if (sessaoDeUsuario.id === colaboradorId) {
        $('span.ion-camera').show();
        $('#conteudo').on('click', 'div[data-js="foto"]', enviarFoto);
        $('input[data-js="alterar-foto"]').off().on('change', alterarFoto);
      }
      else {
        $('div[data-js="apreciacao"]').show();
        $('div[data-js="foto"]').removeClass('alterar-foto');
      }

      _sandbox.notificar('exibir-espaco-para-apreciar', colaboradorId, reconhecimentosDoColaborador);
      _sandbox.notificar('exibir-apreciacoes');
    });
  };

  _self.finalizar = function() {
    $('#conteudo').off();
  }

  function exibirReconhecimentos() {
    var objetoClicado = $(this);

    require(['roteador'], function(roteador) {
      var pilarId = objetoClicado.data('pilar-id');
      var colaboradorId = $("#reconhecidoId").val();

      roteador.navegarPara('/reconhecimentos/' + colaboradorId + '/' + pilarId);
    });
  }

  // TODO: Modular esse envio de foto e aliar com webcomponent
  function enviarFoto() {
    $('input[data-js="alterar-foto"]').trigger('click');
  }

  function alterarFoto() {
    var arquivo = this.files[0];

    if (arquivo.type.indexOf('image/') === -1)
      throw new ViolacaoDeRegra('Apenas imagens podem ser enviadas para seu perfil');

    var reader = new FileReader();

    reader.onload = function(progressEvent) {
      var data = {
        id_do_colaborador: sessaoDeUsuario.id,
        nova_foto: reader.result
      };

      $.post('/login/alterar_foto/', data, function() {
        $('img[data-js="foto"]').attr('src', reader.result);
        $('div[data-js="meu-perfil"] img').attr('src', reader.result);
      });
    };

    if (arquivo)
      reader.readAsDataURL(arquivo);
  }

  return _self;
});

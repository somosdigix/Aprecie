define([
  'template',
  'text!app/perfil/reconhecimentosHistoricosTemplate.html'
], function(template, reconhecimentosHistoricosTemplate) {
  var _self = {};
  var _sandbox;
  var _container = 'div[data-js="reconhecimentos-historicos"]';

  _self.inicializar = function(sandbox, colaboradorId) {
    _sandbox = sandbox;
    _sandbox.escutar('exibir-reconhecimentos-historicos', exibirReconhecimentosHistoricos);

    $('#conteudo')
      .on('click', 'button[data-js="voltar-ao-perfil"]', voltarAoPerfil)
  };

  _self.finalizar = function() {
    $('#conteudo').off();
    _sandbox.removerEscuta('exibir-reconhecimentos-historicos');
  };

  function exibirReconhecimentosHistoricos(colaboradorId) {
    $.getJSON('/reconhecimentos/historico/' + colaboradorId, function(reconhecimentosHistoricos) {
      template.exibirEm(_container, reconhecimentosHistoricosTemplate, reconhecimentosHistoricos);
      $(_container).show();
    });
  };

  function voltarAoPerfil() {
    $(_container).hide();
    _sandbox.notificar('reexibir-perfil');
  }

  return _self;
});

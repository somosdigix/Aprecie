define([
  'jquery',
  'handlebars'
], function($, Handlebars) {
  'use strict';

  var _self = {};

  _self.exibir = function(conteudo, modelo) {
    _self.exibirEm('#conteudo', conteudo, modelo);
  };

  _self.exibirEm = function(container, conteudo, modelo) {
    var conteudo = _self.compilar(conteudo, modelo);
    $(container).empty().append(conteudo);
  };

  _self.acrescentarEm = function(container, conteudo, modelo) {
    var conteudo = _self.compilar(conteudo, modelo);
    $(container).append(conteudo);
  };

  _self.compilar = function(conteudo, modelo) {
    var conteudoCompilado = Handlebars.compile(conteudo);
    return conteudoCompilado(modelo);
  };

  return _self;
});

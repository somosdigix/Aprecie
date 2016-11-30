define([
  'handlebars'
], function(Handlebars) {
  'use strict';

  var icones = {
    'Colaborar sempre': 'colaborar-sempre.jpg',
    'Fazer diferente': 'fazer-diferente.jpg',
    'Focar nas pessoas': 'foco-pessoas.jpg',
    'Planejar, entregar, aprender': 'planejar-entregar.jpg',
  };

  Handlebars.registerHelper('fotoDoPilar', function(valor) {
    var urlBase = '../static/img/';
    var nomeDoValor = valor.nome ? valor.nome.toLocaleLowerCase() : valor.toLocaleLowerCase();

    return urlBase + icones[valor];
  });
});

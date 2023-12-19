﻿define([
  'jquery',
  'template',
  'text!app/toolbar/toolbarTemplate.html',
  'sessaoDeUsuario',
], function ($, template, toolbarTemplate, sessaoDeUsuario) {
  'use strict';

  var toolbarView = {};

  toolbarView.exibir = function (callback) {
    $.getJSON('/login/obter_colaboradores/', function (data) {
      template.exibirEm('header[data-js="toolbar"]', toolbarTemplate, sessaoDeUsuario);

      $('header[data-js="toolbar"]')
        .off()
        .show()
        .on('click', 'a[data-js="pagina-inicial"]', paginaInicial)
        .on('click', 'div[data-js="meu-perfil"]', meuPerfil)
        .on('click', 'div[data-js="tratar-menu-mobile"]', tratarMenuMobile)
        .on('click', 'a[data-js="ranking"]', ranking)
        .on('click', 'a[data-js="sair"]', sair)

      $('div[data-js="buscaDeColaboradores"]').search({
        source: converterParaAutocomplete(data.colaboradores),
        onSelect: selecionar,
        error: {
          noResults: 'Não encontrei ninguém :('
        },
      });

      let buscaInput = document.querySelector("#busca-toolbar");
      buscaInput.addEventListener('keyup', () => {
        buscaInput.value = remover_acentos_espaco(buscaInput.value);
      })

      if (callback)
        callback();
    });
  };

  toolbarView.esconder = function () {
    $('header[data-js="toolbar"]').hide(toolbarTemplate).empty();
  };

  function converterParaAutocomplete(colaboradores) {
    return colaboradores.map(function (colaborador) {
      colaborador.title = remover_acentos_espaco(colaborador.nome);
      return colaborador;
    });
  }

  function remover_acentos_espaco(str) {
    return str.normalize("NFD").replace(/[^a-zA-Z\s]/g, "");
  }

  function selecionar(colaborador) {
    require(['roteador'], function (roteador) {
      $('#colaborador').val('').blur();

      roteador.navegarPara('/perfil/' + colaborador.id);
    });
  }

  function paginaInicial() {
    require(['roteador'], function (roteador) {
      roteador.navegarPara('/paginaInicial');
    });
  }

  function meuPerfil() {
    require(['roteador'], function (roteador) {
      roteador.navegarPara('/perfil/' + sessaoDeUsuario.id);
    });
  }

  function ranking() {
    require(['roteador'], function (roteador) {
      roteador.navegarPara('/ranking');
    });
  }

  function tratarMenuMobile() {
    $('div[data-js="menu-mobile"]').toggleClass('aberto');
  }

  function limparCookies() {
    document.cookie = 'administrador@aprecie.me=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'recursos_humanos@aprecie.me=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'nome@aprecie.me=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'id@aprecie.me=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  }

  function sair() {
    require([
      'app/helpers/cookie',
      'roteador'
    ], function (cookie, roteador) {
      toolbarView.esconder();
      // cookie.limpar(); Substituído pela função limparCookies
      limparCookies();
      window.location = '/';
    });
  }


  return toolbarView;
});



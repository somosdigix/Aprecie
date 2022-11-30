define([
	"jquery",
	"template",
	'text!app/listagemColaboradoresRh/listagemColaboradoresRh.html',
	'text!app/listagemColaboradoresRh/listaColaboradores.html',
], function ($, template, ListagemTemplate, listaColaboradoresTemplate) {
	'use strict';

	var self = {};
	var _sandbox;
	var listagem;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;

		$.getJSON("/login/listagemColaboradoresRh", function (colaboradores) {
			listagem = colaboradores;
			_sandbox.exibirTemplateEm('#conteudo', ListagemTemplate);
			template.exibirEm('div[data-js="lista-colaboradores-rh"]', listaColaboradoresTemplate, listagem);

			$.getJSON('/login/obter_colaboradores/', function (data) {
				$('div[data-js="buscarColaboradorListagem"]').search({
					source: converterParaAutocomplete(data.colaboradores),
					onSelect: filtrarColaboradores,
					error: {
						noResults: 'Não encontrei ninguém :('
					}
				});
			});
		});


	};

	function converterParaAutocomplete(colaboradores) {
		return colaboradores.map(function (colaborador) {
			colaborador.title = colaborador.nome;
			return colaborador;
		});
	}

	function filtrarColaboradores(colaborador) {
		var listagemPorNome = jQuery.extend(true, {}, listagem);
		let nomeColaborador = colaborador.nome;
		let colaboradorFiltrado = listagemPorNome.colaboradores.filter(function (colaborador) {
			if (colaborador.nome.toLowerCase() === nomeColaborador.toLowerCase()) {
				return colaborador;
			}
		})

		template.exibirEm('div[data-js="lista-colaboradores-rh"]', listaColaboradoresTemplate, {"colaboradores": colaboradorFiltrado});
	}

	self.finalizar = function () {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	return self;
});
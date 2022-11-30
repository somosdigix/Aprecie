define([
	"jquery",
	"template",
	'text!app/listagemColaboradoresRh/listagemColaboradoresRh.html',
	'text!app/listagemColaboradoresRh/listaColaboradores.html',
	'text!app/listagemColaboradoresRh/paginacao.html',
], function ($, template, ListagemTemplate, listaColaboradoresTemplate, paginacaoTemplate) {
	'use strict';

	var self = {};
	var _sandbox;
	var listagem;

	self.inicializar = function (sandbox) {
		_sandbox = sandbox;
		_sandbox.exibirTemplateEm('#conteudo', ListagemTemplate);
		$("#select").on("change", carregarListagem);
		carregarListagem();
	};

	function carregarPaginacao(numero_paginas) {
		template.exibirEm('div[data-js="paginacao"]', paginacaoTemplate);
		const divNumerosPaginas = $('div[data-js="numero-paginas"]');

		for (let index = 0; index < numero_paginas; index++) {
			divNumerosPaginas.append('<button class="page-item" id="pagina" value="'+ index + '">' + (index + 1) + '</button>');
		}

		const paginas = $('button[id="pagina"]');
		Array.from(paginas).forEach(paginabtn => {
			paginabtn.addEventListener("click", () => {
				let numero = paginabtn.value;
				template.exibirEm('div[data-js="lista-colaboradores-rh"]', listaColaboradoresTemplate, listagem.colaboradores[numero]);
			})
		});
	}

	function carregarListagem() {
		let tipo_ordenacao = $("#select").val();
		$.getJSON("/login/listagemColaboradoresRh/" + tipo_ordenacao, function (colaboradores) {
			listagem = colaboradores;
			template.exibirEm('div[data-js="lista-colaboradores-rh"]', listaColaboradoresTemplate, listagem.colaboradores[0]);
			carregarPaginacao(listagem.numero_paginas);

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

		template.exibirEm('div[data-js="lista-colaboradores-rh"]', listaColaboradoresTemplate, colaboradorFiltrado);
	}

	self.finalizar = function () {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	return self;
});
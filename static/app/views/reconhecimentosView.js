define([
	'jquery',
	'handlebars',
	'text!partials/reconhecimentosTemplate.html'
], function($, Handlebars, reconhecimentosTemplate) {
	'use strict';
	
	var reconhecimentosView = {};

	reconhecimentosView.exibir = function(cpf) {
		var data = {
			'cpf': cpf
		};
		
		$.post('/reconhecimentos/funcionario/', data, function(reconhecimentosDoFuncionario) {
			var template = Handlebars.compile(reconhecimentosTemplate);
			document.querySelector('#conteudo').innerHTML = template(reconhecimentosDoFuncionario);
		});

		$('#conteudo').off()
			.on('click', '[data-js="reconhecer"]', reconhecer)
			.on('click', '[data-js="voltar"]', voltar);
	};

	function reconhecer() {
		var data = {
			cpf: $(this).data('cpf'),
			valor_id: $(this).data('valor-id'),
			justificativa: 'Justificativa default'
		};

		$.post('/reconhecimentos/reconhecer/', data, function() {
			reconhecimentosView.exibir();
		});
	}

	function voltar() {
		require(['app/views/buscarColaboradorView'], function(buscarColaboradorView) {
			buscarColaboradorView.exibir();
		});
	}

	return reconhecimentosView;
});
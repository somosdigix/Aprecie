var configuracoes = {
	baseUrl: '',

	paths: {
		'text': 'app/lib/requirejs-text/text',
		'jquery': 'app/lib/jquery/dist/jquery',
		'handlebars': 'app/lib/handlebars/handlebars.amd'
	}
};

require.config(configuracoes);

require([
	'jquery',
	'handlebars',
	'text!partials/reconhecimentos.html'
], function($, Handlebars, reconhecimentosTemplate) {
	$.post('/reconhecimentos/funcionario/', {
		'cpf': '00000000000'
	}, function(reconhecimentosDoFuncionario) {
		var template = Handlebars.compile(reconhecimentosTemplate);
		document.querySelector('#conteudo').innerHTML += template(reconhecimentosDoFuncionario);
	});

	$('body').on('click', 'span.ion-plus-round', function() {
		var data = {
			cpf: $(this).data('cpf'),
			valor_id: $(this).data('valor-id'),
			justificativa: 'Justificativa default'
		};

		$.post('/reconhecimentos/reconhecer/', data, function() {
			alert('Reconhecimento realizado com sucesso');
			window.location.reload();
		});
	})
});
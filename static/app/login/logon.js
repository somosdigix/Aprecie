define([
	'text!partials/loginTemplate.html'
], function(loginTemplate) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;

		_sandbox.exibirTemplate('#conteudo', loginTemplate);
		_sandbox.registrarEvento('click', '#conteudo', 'button[data-js="autenticar"]', autenticar);

		ajustarCampos();
	};

	self.finalizar = function() {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	function ajustarCampos() {
		// TODO: Transformar estes ajustes em WebComponents e tirá-los daqui
		$('body').removeClass('body-app').addClass('body-login');
		$('#cpf').inputmask('999.999.999-99').focus().on('keyup', focarDataDeNascimento);
		$('#dataDeNascimento').inputmask('d/m/y');

		if (_sandbox.ehDebug()) {
			$('#cpf').val('00000000000');
			$('#dataDeNascimento').val('01/01/2015');
		}
	}

	function focarDataDeNascimento() {
		var textoSemMascara = this.value.removerMascara();
		var tamanhoDoTextoDigitado = textoSemMascara.length;

		if (tamanhoDoTextoDigitado === 11)
			$('#dataDeNascimento').focus();
	}

	function autenticar() {
		var cpf = $('#cpf').val().replace(/\./g, '').replace('-', '');
		var dataDeNascimento = $('#dataDeNascimento').val();

		_sandbox.notificar('autenticar', cpf, dataDeNascimento);
	};

	return self;
});
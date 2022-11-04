define([
	"jquery",
	'text!app/cadastroDeColaboradores/formularioTemplate.html'
], function($,cadastroTemplate) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function(sandbox) {
		_sandbox = sandbox;

		_sandbox.exibirTemplateEm('#conteudo', cadastroTemplate);
		$("#conteudo").on("click", 'button[data-js="SalvarColaborador"]', validarCpf)
		$('#cpf').inputmask('999.999.999-99')
		$('#conteudo')
        .on('click', 'button[data-js="SalvarColaborador"]', validaFormulario)
	};

	self.finalizar = function() {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	function validaFormulario(){
		if(valida($('#cpf').val())){
			console.log("Cpf ok");
		}
		else{
			console.log("Cpf não ok");
		}
	}
	
	function valida(strCPF) {
		strCPF = strCPF.replaceAll('.', '').replace('-','');
		console.log(strCPF);
		var Soma;
		var Resto;
		Soma = 0;
	  if (strCPF == "00000000000") return false;
	
	  for (var i=1; i<=9; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i);
	  Resto = (Soma * 10) % 11;
	
		if ((Resto == 10) || (Resto == 11))  Resto = 0;
		if (Resto != parseInt(strCPF.substring(9, 10)) ) return false;
	
	  Soma = 0;
		for (i = 1; i <= 10; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
		Resto = (Soma * 10) % 11;
	
		if ((Resto == 10) || (Resto == 11))  Resto = 0;
		if (Resto != parseInt(strCPF.substring(10, 11) ) ) return false;
		return true;
	}

    return self;
});
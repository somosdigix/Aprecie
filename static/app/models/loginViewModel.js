define(function() {
	'use strict';
	
	function LoginViewModel() {
		var self = this;

		self.cpf = $('#cpf').val();
		self.data_de_nascimento = $('#dataDeNascimento').val();
	}

	return LoginViewModel;
})
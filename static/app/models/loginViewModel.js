define(function() {
	'use strict';
	
	function LoginViewModel() {
		var self = this;

		self.cpf = $('#cpf').val().replace(/\./g, '').replace('-', '');
		self.data_de_nascimento = $('#dataDeNascimento').val();
	}

	return LoginViewModel;
})
define([
	'jquery',
	'sessaoDeUsuario'
], function($, sessaoDeUsuario) {
	'use strict';

	function ColaboradorViewModel() {
		var self = this;

		self.cpf = $('#cpf').val();
		self.nome = $('#nomeColaborador').val();
		self.data_de_nascimento = $('#dataDeNascimento').val();
	}

	return ColaboradorViewModel;
});
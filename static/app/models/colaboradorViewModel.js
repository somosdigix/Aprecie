define([
	'jquery',
	'sessaoDeUsuario'
], function($, sessaoDeUsuario) {
	'use strict';

	function ColaboradorViewModel() {
		var self = this;

		self.usuario_id_do_chat = $('#idDiscord').val();
		self.cpf = $('#cpf').val();
		self.nome = $('#nomeColaborador').val();
		self.data_de_nascimento = $('#dataDeNascimento').val();
	}

	return ColaboradorViewModel;
});
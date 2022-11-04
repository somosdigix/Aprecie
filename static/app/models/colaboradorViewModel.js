define([
	'jquery',
	'sessaoDeUsuario'
], function($, sessaoDeUsuario) {
	'use strict';

	function ColaboradorViewModel() {
		var self = this;

		self.id_do_colaborador = sessaoDeUsuario.id;
		self.id_do_usuario_do_chat_do_discord = $('#idDiscord').val();
		self.id_cpf = $('#cpf').val();
		self.id_nome = $('#nomeColaborador').val();
		self.id_data_de_nascimento = $('#dataDeNascimento').val();
	}

	return ColaboradorViewModel;
});
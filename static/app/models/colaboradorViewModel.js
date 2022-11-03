define([
	'jquery',
	'sessaoDeUsuario'
], function($, sessaoDeUsuario) {
	'use strict';

	function ColaboradorViewModel() {
		var self = this;

		self.id_do_colaborador = sessaoDeUsuario.id;
		self.id_do_usuario_do_chat_do_discord = $('#id_usuario_do_chat_do_discord').val();
		self.id_cpf = $('#cpf').val();
		self.id_nome = $('#nome').val();
		self.id_data_de_nascimento = $('#data_de_nascimento').val();
		self.descritivo = $('#descritivo').val();
	}

	return ColaboradorViewModel;
});
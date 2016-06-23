define([
	'jquery',
	'sessaoDeUsuario'
], function($, sessaoDeUsuario) {
	'use strict';

	function ReconhecerViewModel() {
		var self = this;

		self.id_do_reconhecedor = sessaoDeUsuario.id;
		self.id_do_reconhecido = $('#reconhecidoId').val();
		self.id_do_valor = $('#valorId').val();
		self.situacao = $('#situacao').val();
		self.comportamento = $('#comportamento').val();
		self.impacto = $('#impacto').val();
	}

	return ReconhecerViewModel;
});
define([
	'jquery',
	'sessaoDeUsuario'
], function($, sessaoDeUsuario) {
	'use strict';

	function ReconhecerViewModel() {
		var self = this;

		self.id_do_reconhecedor = sessaoDeUsuario.id;
		self.id_do_reconhecido = $('#reconhecidoId').val();
		self.id_do_pilar = $('div.selecione-o-pilar :radio:checked').val();
		self.descritivo = $('#descritivo').val();
	}

	return ReconhecerViewModel;
});


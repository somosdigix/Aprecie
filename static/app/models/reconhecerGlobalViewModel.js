define([
	'jquery',
	'sessaoDeUsuario'
], function($, sessaoDeUsuario) {
	'use strict';

	function ReconhecerGlobalViewModel() {
		var self = this;

		self.id_do_reconhecedor = sessaoDeUsuario.id;
		self.id_do_reconhecido = $('#idDoReconhecido').val();
		self.id_do_pilar = $('div.escolhaPilar :radio:checked').val();
		self.descritivo = $('.elogio').val();
		self.email_do_reconhecedor = 'clevertonxavier@digix.com.br';
		self.email_do_reconhecido = 'clevertonxavier@digix.com.br';
	}

	return ReconhecerGlobalViewModel;
});

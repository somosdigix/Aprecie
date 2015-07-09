define(function() {
	'use strict';
	
	function ReconhecerViewModel(colaboradorId, elemento) {
		var self = this;

		self.id_do_reconhecedor = colaboradorId;
		self.id_do_reconhecido = elemento.data('colaborador-id');
		self.id_do_valor = elemento.data('valor-id');
		self.justificativa = 'Justificativa default';
	}

	return ReconhecerViewModel;
});
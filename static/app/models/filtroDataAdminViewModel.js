define([
	'jquery'
], function($) {
	'use strict';

	function FiltroDataAdminViewModel() {
		var self = this;

		self.data_inicio = $('#data_inicial').val();
		self.data_fim = $('#data_final').val();
	}

	return FiltroDataAdminViewModel;
});
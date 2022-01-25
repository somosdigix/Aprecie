define(function() {
	'use strict';

	var formatadorDeData = {};

	formatadorDeData.obterHoje = function(separador) {
		var hoje = new Date();
		var dia = String(hoje.getDate()).padStart(2, "0");
		var mes = String(hoje.getMonth() + 1).padStart(2, "0");
		var ano = hoje.getFullYear();

		hoje = ano + separador + mes + separador + dia;
		return hoje;
	};

	return formatadorDeData;
});
define(function() {
	var sessaoDeUsuario = {};

	sessaoDeUsuario.id = 0;

	sessaoDeUsuario.definirId = function(id) {
		sessaoDeUsuario.id = id;
	};

	return sessaoDeUsuario;
});
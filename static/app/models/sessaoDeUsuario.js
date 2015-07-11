define(function() {
	var sessaoDeUsuario = {};

	sessaoDeUsuario.id = 0;

	sessaoDeUsuario.preencherDados = function(colaborador) {
		sessaoDeUsuario.id = colaborador.id_do_colaborador;
		sessaoDeUsuario.nome = colaborador.nome_do_colaborador;
	};

	return sessaoDeUsuario;
});
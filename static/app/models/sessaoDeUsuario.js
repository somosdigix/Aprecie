define(function() {
	var sessaoDeUsuario = {};

	sessaoDeUsuario.preencherDados = function(colaborador) {
		sessaoDeUsuario.id = colaborador.id_do_colaborador;
		sessaoDeUsuario.nome = colaborador.nome_do_colaborador;
		sessaoDeUsuario.foto = null;
	};

	return sessaoDeUsuario;
});
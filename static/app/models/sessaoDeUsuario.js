define(function() {
	var sessaoDeUsuario = {};

	sessaoDeUsuario.preencherDados = function(colaborador) {
		sessaoDeUsuario.id = colaborador.id_do_colaborador;
		sessaoDeUsuario.nome = colaborador.nome_do_colaborador;
		sessaoDeUsuario.foto = null;
	};

	sessaoDeUsuario.estaVazia = function() {
		return !sessaoDeUsuario.id && !sessaoDeUsuario.nome;
	}

	return sessaoDeUsuario;
});
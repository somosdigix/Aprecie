function exibirModalReconhecer() {
	var modal = $(".modalReconhecer");

	modal.show();
}

function fecharModal() {
	$(".modalReconhecer").hide();
}

function mostrarResultado(box, num_max, campospan) {
	var contagem_carac = box.length;

	document.getElementById(campospan).innerHTML = contagem_carac + "/220";

	if (contagem_carac >= num_max) {
		document.getElementById(campospan).innerHTML =
			"Limite de caracteres excedido!";
	}
}

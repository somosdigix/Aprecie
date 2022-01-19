function verificaCaracteres(apreciacao){
	if (apreciacao.descricao.length <= 220){
		preencherModal(apreciacao)
	}
	else {
		require(['../static/app/helpers/growl'], function(growl){
			growl
			.deErro()
			.exibir("Não é possível exibir a imagem, a apreciação excedeu o limite de caracteres suportado.");
		})
	}
}

function obterApreciacao(pilar, descricao, reconhecedor, reconhecido) {
	var apreciacao = {
	  pilar : pilar,
	  reconhecido : reconhecido,
	  reconhecedor : reconhecedor,
	  descricao : descricao
	};

	verificaCaracteres(apreciacao)
 }
 
 function preencherModal(apreciacao){
   verificarPilar(apreciacao.pilar);
 
   document.querySelector(".card--titulo").innerHTML = abreviarNome(apreciacao.reconhecido);
   
   document.querySelector(".card--mensagem").innerHTML = apreciacao.descricao;
 
   document.querySelector(".card--mensagemDe").innerHTML = abreviarNome(apreciacao.reconhecedor);
   
   setTimeout(() => gerarModal(), 250);
 }

 function abreviarNome(nome){
	var nome_cortado = nome.split(" ");
	var primeiro_nome = nome_cortado[0];
	var ultimo_nome = nome_cortado[nome_cortado.length - 1];

	return primeiro_nome + " " + ultimo_nome;
}
 
 function verificarPilar(pilar) {
	 var backgroundDiv = document.getElementById("card");
 
	 if (pilar === "Colaborar sempre") {
		 backgroundDiv.style.backgroundImage =
			 "url('../static/img/pilares/colaborarSempre.png')";
	 } else if (pilar === "Fazer diferente") {
		 backgroundDiv.style.backgroundImage =
			 "url('../static/img/pilares/fazerDiferente.png')";
	 } else if (pilar === "Focar nas pessoas") {
		 backgroundDiv.style.backgroundImage =
			 "url('../static/img/pilares/focarNasPessoas.png')";
	 } else if (pilar === "Planejar, entregar e aprender") {
		 backgroundDiv.style.backgroundImage =
			 "url('../static/img/pilares/planejar.png')";
		 document.querySelector(".card--mensagem").style.top = "265px";
	 }
 }
 
 function esconderModal() {
	 document.getElementById("modal").style.visibility = "hidden";
	 document.getElementById("corpo-modal").style.visibility = "hidden";
 }
 
 function gerarModal() {
	 document.getElementById("modal").style.visibility = "visible";
	 document.getElementById("corpo-modal").style.visibility = "visible";
 }
 
 function salvarComo() {
	 html2canvas(document.querySelector("#card")).then(function (canvas) {
		 var uri = canvas.toDataURL();
		 var filename = "file-name.png";
 
		 var link = document.createElement("a");
 
		 if (typeof link.download === "string") {
			 link.href = uri;
			 link.download = filename;
 
			 document.body.appendChild(link);
 
			 link.click();
 
			 document.body.removeChild(link);
		 } else {
			 window.open(uri);
		 }
	 });
 }
define([
	"jquery",
	'text!app/cadastroDeColaboradores/formularioTemplate.html',
	'app/helpers/recursosHumanosHelper',
	"roteador",
	"growl"
], function ($, cadastroTemplate, recursosHumanosHelper, roteador, growl) {
	'use strict';

	var self = {};
	var _sandbox, _colaboradorId;

	self.inicializar = function (sandbox, colaboradorId) {
		_sandbox = sandbox;
		_colaboradorId = colaboradorId;


		if (recursosHumanosHelper.ehRecursosHumanos()) {
			_sandbox.exibirTemplateEm('#conteudo', cadastroTemplate);

			$('#cpf').inputmask('999.999.999-99');
			$('#conteudo').on('focusout', 'input[id="idDiscord"]', validarUserIdDiscord);
			$("#conteudo").on("focusout", 'input[id="cpf"]', validaCPF);
			$("#conteudo").on("focusout", 'input[id="dataDeNascimento"]', validardataDeNascimento);

			if (!colaboradorId) {
				$("#salvarColaborador").click(function (event) {
					event.preventDefault();
					salvarColaborador();
				});
				$("#retornarFormulario").click(function () {
					roteador.navegarPara('/listagemColaboradoresRh');
				});
			} else {

				document.getElementById('tituloPaginaCadastro').textContent = 'Editar Colaborador';
				document.getElementById('salvarColaborador').textContent = 'Concluir Edição';
				document.getElementById('retornarFormulario').textContent = 'Cancelar Edição';

				$.getJSON("/login/obter_colaborador/" + colaboradorId, function (colaborador) {
					$("#nomeColaborador").val(colaborador.nome)
					$("#cpf").val(colaborador.cpf)
					$("#dataDeNascimento").val(colaborador.data_de_nascimento)
					$("#idDiscord").val(colaborador.usuario_id_do_chat)

				});

				$("#salvarColaborador").click(function (event) {
					event.preventDefault();
					editarCadastroColaborador();
				});

				$("#retornarFormulario").click(function () {
					roteador.navegarPara('/listagemColaboradoresRh');
				});
			}

		} else {
			roteador.navegarPara('/paginaInicial');
		}
	};

	function salvarColaborador() {
		validaFormulario();
		var discord = $('#alert-discord').hasClass("sucesso");
		var nome = !$('#alert-nome').hasClass("erro");
		var cpf = $('#alert-cpf').hasClass("sucesso");
		var data_de_nascimento = $('#alert-data').hasClass("sucesso");

		if (discord && nome && cpf && data_de_nascimento) {
			var colaboradores = [{
				cpf: $('#cpf').val(),
				nome: $('#nomeColaborador').val(),
				data_de_nascimento: $('#dataDeNascimento').val(),
				usuario_id_do_chat: $('#idDiscord').val(),
			}]
			var dados = JSON.stringify({
				'colaboradores': colaboradores
			})

			$.post("/login/colaborador/", dados,
				function (retorno) {

					if (retorno.contagem_de_inclusoes == 0 && retorno.cpfs_invalidos.length == 0) {
						mensagem = "Colaborador já existe.";
						growl.deErro().exibir(mensagem);

					} else if (retorno.contagem_de_inclusoes == 0 && retorno.cpfs_invalidos.length == 1) {
						mensagem = "CPF inválido."
						growl.deErro().exibir(mensagem);
					} else {
						var mensagem = "Colaborador cadastrado com sucesso.";
						growl.deSucesso().exibir(mensagem);

						var frm = document.getElementById("formularioCadastro");

						frm.reset();
						setTimeout(() => {
							location.reload();
						}, 1000);
					}

				}).fail(function () {
					growl.deErro().exibir("Colaborador não cadastrado.");
				});
		}
	}

	function editarCadastroColaborador() {
		validaFormulario();
			var discord = $('#alert-discord').hasClass("sucesso");
			var nome = !$('#alert-nome').hasClass("erro");
			var cpf = $('#alert-cpf').hasClass("sucesso");
			var data_de_nascimento = $('#alert-data').hasClass("sucesso");

			if (discord && nome && cpf && data_de_nascimento) {
				var colaborador =
				{
					cpf: $('#cpf').val().replaceAll('.', '').replace('-', ''),
					nome: $('#nomeColaborador').val(),
					data_de_nascimento: $('#dataDeNascimento').val(),
					usuario_id_do_chat: $('#idDiscord').val(),
				}

				var dados = JSON.stringify(colaborador)
				$.post("/login/colaborador/" + _colaboradorId, dados,
					function () {
						growl.deSucesso().exibir("Colaborador editado com sucesso.");
						roteador.navegarPara('/listagemColaboradoresRh')
					}).fail(function () {
						growl.deErro().exibir("Erro ao editar colaborador. Entre em contato com os Dev's responsáveis!");
					});
			}
	}

	function validarUserIdDiscord() {
		var userIdDiscord = $('#idDiscord').val();
		var mensagem = $('#alert-discord');

		if (userIdDiscord.length >= 17) {
			$.ajax({
				type: "GET",
				async: false,
				dataType: "json",
				url: '/login/usario_discord/' + userIdDiscord,
				success: function (data) {
					mensagem.removeClass("erro")
					if (data.status == 200) {
						mensagem.html('Esse id pertence ao usuário <strong>' + data.username + '</strong>.');
						mensagem.removeClass("erro");
						mensagem.addClass("sucesso");
					} else {
						mensagem.html("Esse id nao pertence a um usuário do discord.");
						mensagem.removeClass("sucesso")
						mensagem.addClass("erro")
					}
				}
			})
		} else {
			mensagem.removeClass("erro")
			mensagem.html('A quantidade mínima de números deve ser 17!')
			mensagem.removeClass("sucesso")
			mensagem.addClass("erro")
		}
	}

	self.finalizar = function () {
		_sandbox.limpar('#conteudo');
		_sandbox.removerEvento('#conteudo');
	};

	function validardataDeNascimento() {
		var data = new Date($("#dataDeNascimento").val().replace(/-/g, '/'));
		var dataAtual = new Date();
		dataAtual.setHours(0, 0, 0, 0);


		var mensagem = $('#alert-data');
		if (data < dataAtual) {
			mensagem.text("Data válida");
			mensagem.removeClass("erro")
			mensagem.addClass("sucesso")
		} else {
			mensagem.text("Data inválida");
			mensagem.removeClass("sucesso")
			mensagem.addClass("erro")
		}
	}

	function validaFormulario() {
		validarUserIdDiscord();
		validardataDeNascimento();
		validaCPF();
		validarNome();
	}

	function validarNome() {
		var mensagem = $('#alert-nome');
		var nome = ($('#nomeColaborador').val()).trim();

		if (!nome) {
			mensagem.text("Prencha o nome");
			mensagem.addClass("erro");
		} else {
			mensagem.text("");
			mensagem.removeClass("erro");
		};
	}

	function validaCPF() {

		var mensagem = $('#alert-cpf');


		if (valida($('#cpf').val())) {
			mensagem.text("CPF válido");
			mensagem.removeClass("erro")
			mensagem.addClass("sucesso")

			return true;
		} else {
			mensagem.text("CPF inválido");
			mensagem.removeClass("sucesso")
			mensagem.addClass("erro")

			return false;
		}

	}

	function valida(strCPF) {
		var cpf = strCPF.replaceAll('.', '').replace('-', '');
		if (cpf == '') return false;
		// Elimina CPFs invalidos conhecidos	
		if (cpf.length != 11 ||
			cpf == "00000000000" ||
			cpf == "11111111111" ||
			cpf == "22222222222" ||
			cpf == "33333333333" ||
			cpf == "44444444444" ||
			cpf == "55555555555" ||
			cpf == "66666666666" ||
			cpf == "77777777777" ||
			cpf == "88888888888" ||
			cpf == "99999999999")
			return false;
		// Valida 1o digito	
		var add = 0;
		for (var i = 0; i < 9; i++)
			add += parseInt(cpf.charAt(i)) * (10 - i);
		var rev = 11 - (add % 11);
		if (rev == 10 || rev == 11)
			rev = 0;
		if (rev != parseInt(cpf.charAt(9)))
			return false;
		// Valida 2o digito	
		add = 0;
		for (var i = 0; i < 10; i++)
			add += parseInt(cpf.charAt(i)) * (11 - i);
		rev = 11 - (add % 11);
		if (rev == 10 || rev == 11)
			rev = 0;
		if (rev != parseInt(cpf.charAt(10)))
			return false;
		return true;
	}
	return self;

});
define([
	"jquery",
	'text!app/cadastroDeColaboradores/formularioTemplate.html',
	'app/helpers/recursosHumanosHelper',
	"roteador"
], function ($, cadastroTemplate, recursosHumanosHelper, roteador ) {
	'use strict';

	var self = {};
	var _sandbox;

	self.inicializar = function (sandbox) {
        _sandbox = sandbox;
        if (recursosHumanosHelper.ehRecursosHumanos()) {
            _sandbox.exibirTemplateEm('#conteudo', cadastroTemplate);
            $('#conteudo').on('focusout', 'input[id="idDiscord"]', validarUserIdDiscord);
            $('#cpf').inputmask('999.999.999-99');
            $('#conteudo')
                .on('click', 'button[data-js="SalvarColaborador"]', validaFormulario);
        } else {
            roteador.navegarPara('/paginaInicial');
        }
    };

	function salvarColaborador() {
		if (validaFormulario()) {
			var colaboradores = [
				{
					cpf: $('#cpf').val(),
					nome: $('#nomeColaborador').val(),
					data_de_nascimento: $('#dataDeNascimento').val(),
					usuario_id_do_chat: $('#idDiscord').val(),
				}
			]
			var dados = JSON.stringify({ 'colaboradores': colaboradores })

			$.post("/login/colaborador/", dados,
				function (retorno) {

					if (retorno.contagem_de_inclusoes == 0 && retorno.cpfs_invalidos.length == 0) {
						mensagem = "Colaborador já existe.";
						growl.deErro().exibir(mensagem);

					} else if (retorno.contagem_de_inclusoes == 0 && retorno.cpfs_invalidos.length == 1) {
						mensagem = "CPF inválido."
						growl.deErro().exibir(mensagem);
					}
					else {
						var mensagem = "Colaborador cadastrado com sucesso.";
						growl.deSucesso().exibir(mensagem);
						
							var frm = document.getElementById("formularioCadastro");
							
							frm.reset();  
							setTimeout(() => {
								location.reload();
							  }, 3000);
					}

	
				}).fail(function () {
					growl.deErro().exibir("Colaborador não cadastrado.");
				});
		if (recursosHumanosHelper.ehRecursosHumanos()) {
			_sandbox.exibirTemplateEm('#conteudo', cadastroTemplate);
			$('#conteudo').on('focusout', 'input[id="idDiscord"]', validarUserIdDiscord);
			$('#cpf').inputmask('999.999.999-99');
			$('#conteudo')
				.on('click', 'button[data-js="SalvarColaborador"]', validaFormulario);
		} else {
			roteador.navegarPara('/paginaInicial');
		}
	};

	function validarUserIdDiscord() {
		var userIdDiscord = $('#idDiscord').val();
		var chaveDiscord = ''
		$.ajax({
			beforeSend: function (request) {
				request.setRequestHeader("Authorization", 'Bot' + chaveDiscord);
			},
			dataType: "json",
			url: 'https://discord.com/api/v10/users/' + userIdDiscord,
			success: function (data) {
				// Se deu certo
			},
			statusCode: {
				404: function () {
					// Se deu errado
				}
			}
		});
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

			return true;
		} else {
			mensagem.text("Data inválida");
			mensagem.removeClass("sucesso")
			mensagem.addClass("erro")

			return false;
		}
	}

	function validaFormulario() {
		validardataDeNascimento();
		validaCPF();
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
}

});
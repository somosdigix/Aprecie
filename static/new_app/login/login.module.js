import template from './login.template.html';

export default class Login {
  constructor(sandbox) {
    this.sandbox = sandbox;
    this.viewModel = {
      cpf: '000.000.000-00',
      dataDeNascimento: '01/01/2015',
      autenticar: () => this.autenticar()
    };
  }

  iniciar() {
    this.sandbox.modelBinder.iniciar('main[data-js="conteudo"]', template, this.viewModel);

    this.sandbox.dom('#cpf').focus();
    this.sandbox.dom('main[data-js="conteudo"]').event('keyup', '#cpf', () => this.focarDataDeNascimento());
  }

  focarDataDeNascimento() {
    var tamanhoDoTextoDigitado = this.viewModel.cpf.removerMascara().length;

    if (tamanhoDoTextoDigitado === 11)
      this.sandbox.dom('#dataDeNascimento').focus();
  }

  autenticar() {
    this.sandbox.mediador.notificar('autenticar', this.viewModel.cpf, this.viewModel.dataDeNascimento);
  }
}

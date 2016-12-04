export default class Autenticacao {
  constructor(sandbox) {
    this.sandbox = sandbox;
  }

  iniciar() {
    this.sandbox.mediador.escutar('autenticar', this, this.validarAutenticacao);
  }

  finalizar() {
    this.sandbox.mediador.removerEscuta('autenticar');
  }

  validarAutenticacao(cpf, dataDeNascimento) {
    this.validarOperacao(cpf, dataDeNascimento);
    this.sandbox.api.login.autenticar(cpf, dataDeNascimento).then(() => this.autenticar());
  }

  autenticar(colaborador) {
    // this.sandbox.preencherSessao(colaborador);
    // this.sandbox.preencherCookie(colaborador);

    this.sandbox.roteador.navegarPara('/timeline');
  }

  validarOperacao(cpf, dataDeNascimento) {
    if (cpf === '' || cpf === undefined)
      throw new window.ViolacaoDeRegra('CPF deve ser informado');

    if (dataDeNascimento === '' || dataDeNascimento === undefined)
      throw new window.ViolacaoDeRegra('Data de nascimento deve ser informada');
  }
}

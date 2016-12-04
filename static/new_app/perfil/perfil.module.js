import ko from 'knockout';
import template from './perfil.template.html';

export default class Perfil {
  constructor(sandbox) {
    this.sandbox = sandbox;
    this.viewModel = {
      id: ko.observable(),
      nome: ko.observable()
    };
  }

  iniciar() {
    this.sandbox.modelBinder.iniciar('div[data-js="perfil"]', template, this.viewModel);    

    this.sandbox.api.reconhecimentos.obterPorPilar(7).then(reconhecimentosDoColaborador => {
      this.viewModel.id(reconhecimentosDoColaborador.id);
      this.viewModel.nome(reconhecimentosDoColaborador.nome);
    });
  }

  finalizar() {

  }
}

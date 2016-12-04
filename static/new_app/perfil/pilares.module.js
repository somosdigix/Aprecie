import ko from 'knockout';
import template from './pilares.template.html';

export default class Pilares {
  constructor(sandbox) {
    this.sandbox = sandbox;
    this.viewModel = {
      pilares: ko.observableArray()
    };
  }

  iniciar() {
    this.sandbox.modelBinder.iniciar('div[data-js="pilares"]', template, this.viewModel);

    this.sandbox.api.reconhecimentos.obterPorPilar(7).then(reconhecimentosDoColaborador => {
      this.viewModel.pilares(reconhecimentosDoColaborador.pilares);
    });
  }

  finalizar() {
  }

  exibirReconhecimentos() {
  }
}

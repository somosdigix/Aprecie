import template from './reconhecimentos.template.html';

export default class Reconhecimentos {
  constructor(sandbox) {
    this.sandbox = sandbox;
    this.viewModel = {};
  }

  iniciar() {
    this.sandbox.modelBinder.iniciar('div[data-js="reconhecimentos"]', template, this.viewModel);    
  }

  finalizar() {

  }
}

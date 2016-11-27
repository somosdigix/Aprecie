import template from './reconhecer.template.html';

export default class Reconhecer {
  constructor(sandbox) {
    this.sandbox = sandbox;
    this.viewModel = {};
  }

  iniciar() {
    this.sandbox.modelBinder.iniciar('div[data-js="reconhecer"]', template, this.viewModel);    
  }

  finalizar() {

  }
}

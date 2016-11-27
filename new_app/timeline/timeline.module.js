import template from './timeline.template.html';

export default class Timeline {
  constructor(sandbox) {
    this.sandbox = sandbox;
    this.viewModel = {
      reconhecimentos: []
    };
  }

  iniciar() {
    this.sandbox.api.reconhecimentos.obterTodas().then(reconhecimentos => {
      this.viewModel.reconhecimentos = reconhecimentos;
      this.sandbox.modelBinder.iniciar('main[data-js="conteudo"]', template, this.viewModel);
    });
  }

  finalizar() {
  }
}

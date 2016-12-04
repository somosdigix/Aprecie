class Mediador {
  constructor() {
    this.eventos = {};
  }

  escutar(nomeDoEvento, modulo, callback) {
    this._validarSeEventoEstaDuplicado(nomeDoEvento, modulo);

    const evento = this.eventos[nomeDoEvento];

    if (!evento)
      this.eventos[nomeDoEvento] = [];

    this.eventos[nomeDoEvento].push({
      modulo: modulo,
      callback: callback
    });
  }

  removerEscuta(nomeDoEvento) {
    let evento = this.eventos[nomeDoEvento];

    if (evento)
      delete this.eventos[nomeDoEvento];
  }

  notificar(nomeDoEvento, ...dados) {
    const evento = this.eventos[nomeDoEvento];

    if (evento)
      evento.forEach((handler) => handler.callback.apply(handler.modulo, dados));
  }

  _validarSeEventoEstaDuplicado(nomeDoEvento, modulo) {
    const evento = this.eventos[nomeDoEvento];

    if (evento)
      evento.forEach((handler) => {
        if (handler.modulo == modulo)
          throw new Error('Evento já registrado para este módulo');
      });
  }
}

module.exports = Mediador;

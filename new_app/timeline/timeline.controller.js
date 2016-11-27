import Sandbox from '../sandbox';
import Timeline from './timeline.module';

export default class TimelineController {
  constructor() {
    const sandbox = new Sandbox();

    this.modulos = [
      new Timeline(sandbox)
    ];
  }

  iniciar() {
    this.modulos.forEach(modulo => modulo.iniciar());
  }

  finalizar() {
    this.modulos.forEach(modulo => modulo.finalizar());
  }
}

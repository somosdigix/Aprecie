import Sandbox from '../sandbox';
import Perfil from './perfil.module';
import Reconhecer from './reconhecer.module';
import Pilares from './pilares.module';
import Reconhecimentos from './reconhecimentos.module';

export default class PerfilController {
  constructor() {
    const sandbox = new Sandbox();

    this.modulos = [
      new Perfil(sandbox),
      new Reconhecer(sandbox),
      new Pilares(sandbox),
      new Reconhecimentos(sandbox)
    ];
  }

  iniciar() {
    // TODO: Pensar em como encapsular o html base fornecido pelo controller, que
    // irá criar os placeholders para que os módulos se encaixem perfeitamente na tela
    this.criarTemplateBase();

    this.modulos.forEach(modulo => modulo.iniciar());
  }

  finalizar() {
    this.modulos.forEach(modulo => {
      if (modulo.finalizar)
        modulo.finalizar();
    });
  }

  criarTemplateBase() {
    document.querySelector('main[data-js="conteudo"]').innerHTML = `
      <div>
        <div data-js="perfil"></div>
        <div data-js="reconhecer"></div>
      </div>

      <div>
        <div data-js="pilares"></div>
        <div data-js="reconhecimentos"></div>
      </div>
    `;
  }
}

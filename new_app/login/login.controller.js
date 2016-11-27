import Sandbox from '../sandbox';
import Login from './login.module';
import Autenticacao from './autenticacao.module';

export default class LoginController {
  constructor() {
    const sandbox = new Sandbox();

    this.modulos = [
      new Login(sandbox),
      new Autenticacao(sandbox)
    ];
  }

  iniciar() {
    this.modulos.forEach(modulo => modulo.iniciar());
  }

  finalizar() {
    this.modulos.forEach(modulo => {
      if (modulo.finalizar)
        modulo.finalizar();
    });
  }
}

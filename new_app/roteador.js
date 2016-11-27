import Router from 'director';
import ControllerFactory from './controllerFactory';
import LoginController from './login/login.controller';
import TimelineController from './timeline/timeline.controller';
import PerfilController from './perfil/perfil.controller';

let _router = null;
let _controllerFactory = new ControllerFactory();

export default class Roteador {
  static configurar() {
    const login = () => {
      _controllerFactory.iniciar(LoginController);
    };

    const timeline = () => {
      _controllerFactory.iniciar(TimelineController);
    };

    const perfil = () => {
      _controllerFactory.iniciar(PerfilController);
    };

    const rotas = {
      '/': login,
      '/timeline': timeline,
      '/perfil/:colaboradorId': perfil
    };

    _router = Router.Router(rotas);
    _router.init();
  }

  static navegarPara(rota) {
    window.location = '#' + rota;
  }
}


import Mediador from './mediador';
import Roteador from './roteador';
import dom from './base-lib/dom';
import modelBinder from './base-lib/modelBinder';
import http from './base-lib/http';

export default class Sandbox {
  constructor() {
    this.mediador = new Mediador();
    this.dom = dom;
    this.modelBinder = modelBinder;
    this.api = new Api();
    this.roteador = Roteador;
  }
}

class Api {
  get login() {
    return LoginApi;
  }

  get reconhecimentos() {
    return ReconhecimentosApi;
  }
}

class LoginApi {
  static autenticar(cpf, dataDeNascimento) {
    const parametros = {
      cpf: cpf.replace(/\./g, '').replace(/-/g, ''),
      data_de_nascimento: dataDeNascimento
    };

    return http.post('http://localhost:3000/login/entrar/', parametros);
  }
}

class ReconhecimentosApi {
  static obterTodas() {
    return http.getJson('http://localhost:3000/reconhecimentos/ultimos/');
  }

  static obterPorPilar(idDoColaborador) {
    return http.getJson('http://localhost:3000/reconhecimentos/colaborador/' + idDoColaborador);
  }
}

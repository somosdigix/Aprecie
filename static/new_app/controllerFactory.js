let _controllerAtivo = null;

export default class ControllerFactory {
  iniciar(controller) {
    if (_controllerAtivo && _controllerAtivo.finalizar)
      _controllerAtivo.finalizar();

    _controllerAtivo = new controller();
    _controllerAtivo.iniciar();
  }
}

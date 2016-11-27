import ko from 'knockout';
import Dom from './dom';
import Mascaras from '../widgets/mascaras';

export default class ModelBinder {
  static iniciar(seletor, template, viewModel) {
    const elemento = document.querySelector(seletor);

    Dom(elemento).append(template);
    ko.cleanNode(elemento);
    ko.applyBindings(viewModel, elemento);

    Mascaras.aplicar();
  }
}

import vanillaMasker from 'vanilla-masker';
import Dom from '../base-lib/dom';

export default class Mascaras {
  static aplicar() {
    const mascaras = {
      cpf: '999.999.999-99',
      data: '99/99/9999'
    };

    let camposComMascara = document.querySelectorAll('[data-mascara]');

    camposComMascara.forEach(campo => {
      const mascara = mascaras[Dom(campo).getData('mascara')];

      vanillaMasker(campo).unMask();
      vanillaMasker(campo).maskPattern(mascara);
    });
  }
}

import './styles/estilo.css';
import './styles/perfil.css';
import Roteador from './roteador';
import './errors/violacaoDeRegra';

Roteador.configurar();

// TODO: Criar um configurador de funções globais
localStorage.debug = '';
NodeList.prototype.forEach = Array.prototype.forEach;

Object.defineProperty(String.prototype, 'removerMascara', {
  enumerable: false,
  value: function () {
    return this.replace(/-/g, '').replace(/\./g, '').replace(/_/g, '');
  }
});

window.onerror = function(mensagem, fonte, linha, coluna, erro) {
  if (erro.constructor.name !== 'ViolacaoDeRegra' &&
    erro.constructor.name !== 'ErroInesperado')
    return;

  alert(erro.message);
};

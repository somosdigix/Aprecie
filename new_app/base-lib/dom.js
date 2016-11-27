class DomElement {
  constructor(elements) {
    this.elements = Array.from(elements);
    this.element = this.elements[0];
    this.itsJustOneElement = elements.length === 1;
  }

  _map(callback) {
    const mappedContent = this.elements.map(callback);

    return this.itsJustOneElement ? mappedContent[0] : mappedContent;
  }

  getAttr(attrName) {
    return this._map((element) => element.getAttribute(attrName));
  }

  getData(dataName) {
    return this._map((element) => element.getAttribute(`data-${dataName}`));
  }

  getHtml() {
    return this._map((element) => element.innerHTML);
  }

  getValue() {
    return this._map((element) => element.value);
  }

  value(newValue) {
    this.elements.forEach((element) => element.value = newValue);
    return this;
  }

  append(content) {
    this.elements.forEach((element) => element.innerHTML = content);
    return this;
  }

  empty() {
    this.elements.forEach((element) => element.innerHTML = '');
    return this;
  }

  addClass(...classes) {
    this.elements.forEach((element) => element.classList.add(...classes));
    return this;
  }

  removeClass(...classes) {
    this.elements.forEach((element) => element.classList.remove(...classes));
    return this;
  }

  focus() {
    this.element.focus();
    return this;
  }

  event(eventName, target, handler) {
    this.element.addEventListener(eventName, (event) => {
      const element = event.target;
      const isTheSameType = element.matches(target);

      if (isTheSameType)
        handler.apply(this, [element]);
    }, false);

    return this;
  }

  trigger(eventName) {
    this.elements.forEach((element) => {
      let event = document.createEvent('HTMLEvents');
      event.initEvent(eventName, true, true);

      element.dispatchEvent(event);
    });

    return this;
  }
}

class Dom {
  static select(selector) {
    let element;
    const isSelector = typeof(selector) === 'string';
    const isNotHtmlElement = !(selector instanceof window.HTMLElement);

    if (isSelector) {
      element = document.querySelectorAll(selector);

      if (element.length === 0)
        throw new Error(`Elemento com o seletor '${selector}' não foi encontrado`);
    }

    else if (isNotHtmlElement)
      throw new Error('Elemento informado não é um elemento HTML válido');

    else
        element = [selector];

    return new DomElement(element);
  }
}

module.exports = (selector) => {
  return Dom.select(selector);
};

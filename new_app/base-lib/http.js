import $ from 'jquery';

export default class Http {
  static getJson(url, parameters) {
    return new Promise((resolve, reject) => {
      const done = _createDoneHandler(resolve);
      const fail = _createFailHandler(reject);

      $.getJSON(url, parameters).done(done).fail(fail);
    });
  }

  static post(url, parameters) {
    return new Promise((resolve, reject) => {
      const done = _createDoneHandler(resolve);
      const fail = _createFailHandler(reject);

      $.post(url, parameters).done(done).fail(fail);
    });
  }
}

const _createDoneHandler = (resolve) => {
  return response => resolve(response);
};

const _createFailHandler = (reject) => {
  return error => reject(error);
};

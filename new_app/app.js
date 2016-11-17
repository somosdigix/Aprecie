import './styles/index.css';

import debug from 'debug';
const log = debug('app:log');

debug.enable('*');
log('Log ok');

class Animal {
  constructor() {
    this.name = 'asd';
  }
}

new Animal();

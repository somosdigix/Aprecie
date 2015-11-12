function ErroInesperado(mensagem) {
	'use strict';

	var self = this;

	self.message = mensagem;
	self.stack = (new Error()).stack;
}
ErroInesperado.prototype = Object.create(Error.prototype);
ErroInesperado.prototype.name = "ErroInesperado";
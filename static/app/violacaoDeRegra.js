function ViolacaoDeRegra(mensagem) {
	'use strict';

	var self = this;

	self.message = mensagem;
	self.stack = (new Error()).stack;
}
ViolacaoDeRegra.prototype = Object.create(Error.prototype);
ViolacaoDeRegra.prototype.name = "ViolacaoDeRegra";
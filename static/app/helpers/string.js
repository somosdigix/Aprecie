String.prototype.removerMascaras = function() {
	return this.replace(/-/g, '').replace(/\./g, '').replace(/_/g, '');
};
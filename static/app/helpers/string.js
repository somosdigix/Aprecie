Object.defineProperty(String.prototype, "removerMascara", {
	enumerable: false,
	value: function () {
		return this.replace(/-/g, '').replace(/\./g, '').replace(/_/g, '');
	}
});
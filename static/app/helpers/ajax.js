window.app = window.app || {};

window.app.ajax = (function() {
	var self = {};

	self.post = function(url, callback) {
		var xmlHttpRequest = new XMLHttpRequest();

		xmlHttpRequest.onreadystatechange = function() {
			if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) {
				var resultados = JSON.parse(xmlHttpRequest.responseText);
				callback(resultados);
			}
		};

		xmlHttpRequest.open('POST', url, true);
		xmlHttpRequest.send();
	};

	return self;
}());
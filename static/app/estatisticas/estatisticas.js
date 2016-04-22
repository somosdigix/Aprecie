define([
	'text!app/estatisticas/estatisticas.template.html'
], function(estatisticasTemplate) {
	'use strict';

	var _self = {};
	var _sandbox;

	_self.inicializar = function(sandbox) {
		_sandbox = sandbox;
		_sandbox.acrescentarTemplateEm('#conteudo', estatisticasTemplate);

		google.charts.load('current', {
			packages: ['corechart', 'bar']
		});

		google.charts.setOnLoadCallback(desenharGraficos);
	};

	function desenharGraficos() {
		desenharApreciados();
		desenharApreciadores();
		desenharValoresApreciados();
	}

	function desenharApreciados() {
		var data = google.visualization.arrayToDataTable([
			['Colaborador', 'Apreciações', {
				role: 'style'
			}],
			['João', 11, '#fb9a09'],
			['José', 11, '#fb9a09'],
			['Maria', 9, '#fb9a09']
		]);

		var options = {
			title: 'Pessoas mais apreciadas',
			isStacked: true,
			hAxis: {
				title: 'Apreciações',
				minValue: 0,
			},
			vAxis: {
				title: 'Colaborador'
			},
			legend: {
				position: 'none'
			}
		};

		var chart = new google.visualization.BarChart(document.getElementById('colaboradoresMaisApreciados'));
		chart.draw(data, options);
	}

	function desenharApreciadores() {
		var data = google.visualization.arrayToDataTable([
			['Colaborador', 'Apreciações', {
				role: 'style'
			}],
			['Huguinho', 19, '#fb9a09'],
			['Zezinho', 11, '#fb9a09'],
			['Luizinho', 10, '#fb9a09']
		]);

		var options = {
			title: 'Pessoas que mais apreciaram',
			isStacked: true,
			hAxis: {
				title: 'Apreciações',
				minValue: 0,
			},
			vAxis: {
				title: 'Colaborador'
			},
			legend: {
				position: 'none'
			}
		};

		var chart = new google.visualization.BarChart(document.getElementById('colaboradoresQueMaisApreciaram'));
		chart.draw(data, options);
	}

	function desenharValoresApreciados() {
		var data = google.visualization.arrayToDataTable([
			['Valor', 'Quantidade', {
				role: 'style'
			}],
			['Colaboração', 67, '#fb9a09'],
			['Resultado', 44, '#fb9a09'],
			['Inquietude', 25, '#fb9a09'],
			['Alegria', 16, '#fb9a09'],
			['Relacionamento', 15, '#fb9a09'],
			['Responsabilidade', 13, '#fb9a09'],
			['Segurança', 6, '#fb9a09']
		]);

		var options = {
			title: 'Valores apreciados',
			isStacked: true,
			hAxis: {
				title: 'Valores'
			},
			vAxis: {
				title: 'Quantidade'
			},
			legend: {
				position: 'none'
			},
			height: 300
		};

		var chart = new google.visualization.ColumnChart(document.getElementById('quantidadeDeApreciacoesPorValor'));
		chart.draw(data, options);
	}

	return _self;
});
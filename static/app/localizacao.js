define([
	"globalize", 
	'json!cldr-data/supplemental/likelySubtags.json',
	'json!cldr-data/main/pt/numbers.json',
	'json!cldr-data/supplemental/numberingSystems.json',
	'json!cldr-data/main/pt/ca-gregorian.json',
	'json!cldr-data/main/pt/timeZoneNames.json',
	'json!cldr-data/supplemental/timeData.json',
	'json!cldr-data/supplemental/weekData.json',

	"globalize/date",
	"globalize/number"
], function(
	Globalize,
	likelySubtags,
	ptNumbers,
	numberingSystems,
	ptGregorian,
	ptTimezones,
	timeData,
	weekData
) {
	var localizacao = {};
	Globalize.load(likelySubtags, ptNumbers, numberingSystems, ptGregorian, ptTimezones, timeData, weekData);
	var localidade = Globalize('pt');

	localizacao.formatarData = function(data) {
		var formatoDaApi = {raw: 'yyyy-MM-dd'};
		var formatoDeVisualizacao = {raw: 'd \'de\' MMMM \'de\' y'};
		return localidade.formatDate(localidade.parseDate(data, formatoDaApi), formatoDeVisualizacao);
	};

	return localizacao;
});
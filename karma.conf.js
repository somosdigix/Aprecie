// Karma configuration
// Generated on Sun Jul 12 2015 14:01:03 GMT-0400 (Central Brazilian Standard Time)

module.exports = function(config) {
	config.set({

		// base path that will be used to resolve all patterns (eg. files, exclude)
		basePath: 'static',


		// frameworks to use
		// available frameworks: https://npmjs.org/browse/keyword/karma-adapter
		frameworks: ['jasmine', 'requirejs'],


		// list of files / patterns to load in the browser
		files: [
			'test-main.js',
			'lib/promise-polyfill/Promise.js',
			'app/helpers/string.js', {
				pattern: 'partials/*.html',
				included: false
			}, {
				pattern: 'lib/requirejs-text/text.js',
				included: false
			}, {
				pattern: 'lib/jquery/dist/jquery.js',
				included: false
			}, {
				pattern: 'lib/jquery-ui/jquery-ui.js',
				included: false
			}, {
				pattern: 'lib/jquery.inputmask/dist/jquery.inputmask.bundle.js',
				included: false
			}, {
				pattern: 'lib/blockUI/jquery.blockUI.js',
				included: false
			}, {
				pattern: 'lib/handlebars/handlebars.amd.js',
				included: false
			}, {
				pattern: 'lib/director/build/director.js',
				included: false
			}, {
				pattern: 'app/**/*.js',
				included: false
			}, {
				pattern: 'test/**/*.spec.js',
				included: false
			}
		],

		// list of files to exclude
		exclude: [],

		// preprocess matching files before serving them to the browser
		// available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
		preprocessors: {},


		// test results reporter to use
		// possible values: 'dots', 'progress'
		// available reporters: https://npmjs.org/browse/keyword/karma-reporter
		reporters: ['mocha'],

		junitReporter: {
			outputDir: '', // results will be saved as $outputDir/$browserName.xml
			outputFile: undefined, // if included, results will be saved as $outputDir/$browserName/$outputFile
			suite: '', // suite will become the package name attribute in xml testsuite element
			useBrowserName: true // add browser name to report and classes names
		},

		// web server port
		port: 9876,


		// enable / disable colors in the output (reporters and logs)
		colors: true,


		// level of logging
		// possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
		logLevel: config.LOG_INFO,


		// enable / disable watching file and executing tests whenever any file changes
		autoWatch: true,


		// start these browsers
		// available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
		browsers: ['PhantomJS'],


		// Continuous Integration mode
		// if true, Karma captures browsers, runs the tests and exits
		singleRun: false
	});
};
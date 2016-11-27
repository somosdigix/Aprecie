var gulp = require('gulp');
var browserSync = require('browser-sync').create();
var sourcemaps = require('gulp-sourcemaps');
var sass = require('gulp-sass');

gulp.task('serve', ['sass'], function() {
	browserSync.init({
		proxy: 'localhost:8000',
		notify: false
	});

	gulp.watch('static/css/**/*.sass', ['sass']);
	gulp.watch('static/**/*.html').on('change', browserSync.reload);
	gulp.watch('static/app/**/*.js').on('change', browserSync.reload);
});

gulp.task('sass', function() {
	gulp.src('static/css/**/*.sass')
		.pipe(sourcemaps.init())
		.pipe(sass({
			indentedSyntax: true
		}).on('error', sass.logError))
		.pipe(sourcemaps.write())
		.pipe(gulp.dest('./static/css'))
		.pipe(browserSync.stream());
});

gulp.task('sass:watch', function() {
	gulp.watch('static/css/**/*.sass', ['sass']);
});

gulp.task('default', ['serve']);

var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('sass', function() {
	gulp.src('css/**/*.sass')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest('./css'));
});

gulp.task('sass:watch', function() {
	gulp.watch('css/**/*.sass', ['sass']);
});
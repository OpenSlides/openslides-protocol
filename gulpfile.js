// Run tasks with $ ./node_modules/.bin/gulp
require('es6-promise').polyfill();

var gulp = require('gulp'),
    gettext = require('gulp-angular-gettext'),
    jshint = require('gulp-jshint'),
    path = require('path'),
    templateCache = require('gulp-angular-templatecache');

/**
 * Default tasks to be run before start.
 */

// Catches all template files concats them to one file js/templates.js.
gulp.task('templates', function () {
    return gulp.src(path.join('**', 'static', 'templates', '**', '*.html'))
        .pipe(templateCache('templates.js', {
            module: 'OpenSlidesApp.openslides_protocol.templates',
            standalone: true,
            moduleSystem: 'IIFE',
            transformUrl: function (url) {
                var pathList = url.split(path.sep);
                pathList.shift();
                return pathList.join(path.sep);
            },
        }))
        .pipe(gulp.dest(path.join('static', 'js', 'openslides_protocol')));
});
// Compiles translation files (*.po) to *.json and saves them in the directory 'i18n'.
gulp.task('translations', function () {
    return gulp.src(path.join('openslides_protocol', 'locale', 'angular-gettext', '*.po'))
        .pipe(gettext.compile({
            format: 'json'
        }))
        .pipe(gulp.dest(path.join('static', 'i18n', 'openslides_protocol')));
});

// Gulp default task. Runs all other tasks before.
gulp.task('default', ['translations', 'templates'], function () {});

// Watches changes in JavaScript and templates.
 gulp.task('watch', ['templates'], function   () {
    gulp.watch([
        path.join('**', 'static', 'templates', '**', '*.html')
    ], ['templates']);
 });

/**
 * Extra tasks that have to be called manually. Useful for development.
 */

// Extracts translatable strings using angular-gettext and saves them in file
// locale/angular-gettext/template-en.pot.
gulp.task('pot', function () {
    return gulp.src([
            'openslides_protocol/static/templates/*/*.html',
            'openslides_protocol/static/js/*/*.js',
        ])
        .pipe(gettext.extract('template-en.pot', {}))
        .pipe(gulp.dest(path.join('openslides_protocol', 'locale', 'angular-gettext')));
});

// Checks JavaScript using JSHint
gulp.task('jshint', function () {
    return gulp.src([
            'gulpfile.js',
            path.join('openslides_protocol', 'static', 'js', 'openslides_protocol', '*.js'),
        ])
        .pipe(jshint())
        .pipe(jshint.reporter('default'))
        .pipe(jshint.reporter('fail'));
});

module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    
    sprite: {
      all: {
        src: 'goorchids/core/static/images/build-sprites/*.png',
        destImg: 'goorchids/core/static/images/sprites/sprite.png',
        destCSS: 'goorchids/core/static/sass/ui/_sprites.scss',
        imgPath: '../images/sprites/sprite.png',
        cssFormat: 'scss'
      }
    },
    
    sass: {
      dev: {
        src: 'goorchids/core/static/sass/app.scss',
        dest: 'goorchids/core/static/css/app.css',
        options: {
          style: 'expanded'
        }
      },
      prod: {
        src: 'goorchids/core/static/sass/app.scss',
        dest: 'goorchids/core/static/css/app.min.css',
        options: {
          style: 'compact'
        }
      }
    },
    
    jshint: {
      files: ['Gruntfile.js'],
      options: {
        // options here to override JSHint defaults
        globals: {
          jQuery: true,
          console: true,
          module: true,
          document: true
        }
      }
    },
    
    regarde: {
      jshint: {
        files: ['Gruntfile.js'],
        tasks: 'jshint'
      },
      stylesheets: {
        files: 'goorchids/core/static/sass/**/*.scss',
        tasks: 'sass'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-regarde');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-spritesmith');

  grunt.registerTask('default', ['sass', 'jshint']);

};
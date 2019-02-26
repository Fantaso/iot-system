module.exports = function(grunt) {


  'use strict';    
  global.myLayout    = grunt.option('Layout'); // Layout name

  // write custome selected theme.scss file which will import in style.scss and materialize.scss 
  grunt.file.write('sass/theme.scss', '@import "themes/' + grunt.option('Layout') + '/theme";');

  // configure the tasks
  grunt.initConfig({    

    //Copy all content for dist folder
    copy: {
      main: {
        src: ['**/*',  '!**/node_modules/**',  '!**/sass/**',  '!**/dist/**',  '!**/bin/**',  '!**/temp/**', '!**/templates/**','!.gitgnore','!package.json','!package.js','!bower.json','!Gruntfile.js'],
        expand: true,
        cwd: '',
        dest: 'dist',
      }
    },

    //SASS Compile css
    sass: {
      main: {
        options: {
          outputStyle: 'expanded',
          sourcemap: false,
        },
        files: {
          ['css/themes/'+myLayout+'/materialize.css']: 'sass/materialize.scss',
          ['css/themes/'+myLayout+'/style.css']: 'sass/style.scss',
          'css/layouts/style-fullscreen.css': 'sass/theme-components/layouts/style-fullscreen.scss',
          'css/layouts/style-horizontal.css': 'sass/theme-components/layouts/style-horizontal.scss',
          'css/custom/custom.css': 'sass/custom/custom.scss'
        }
      },
      dist: {
        options: {
          outputStyle: 'compressed',
          sourcemap: false
        },
        files: {
          ['css/themes/'+myLayout+'/materialize.min.css']: 'sass/materialize.scss',
          ['css/themes/'+myLayout+'/style.min.css']: 'sass/style.scss',
          'css/layouts/style-fullscreen.min.css': 'sass/theme-components/layouts/style-fullscreen.scss',
          'css/layouts/style-horizontal.min.css': 'sass/theme-components/layouts/style-horizontal.scss',
          'css/custom/custom.min.css': 'sass/custom/custom.scss'
        }
      }      
    },

    // PostCss Autoprefixer
    postcss: {
      options: {
        processors: [
        require('autoprefixer')({
          browsers: [
          'last 2 versions',
          'Chrome >= 30',
          'Firefox >= 30',
          'ie >= 10',
          'Safari >= 8']
        })
        ]
      },
      main: {
        files: {
          'css/materialize.css': 'css/materialize.css',
          ['css/themes/'+myLayout+'/style.css']: 'css/themes/'+myLayout+'/style.css',
          'css/layouts/style-fullscreen.css': 'css/layouts/style-fullscreen.css',
          'css/layouts/style-horizontal.css': 'css/layouts/style-horizontal.css',
          'css/custom/custom.css': 'css/custom/custom.css'
        }
      },
    },

    //Browser Sync integration
    browserSync: {
      bsFiles: ["bin/*.js", "bin/*.css", "!**/node_modules/**/*"],
      options: {
        server: {
              baseDir: "./" // make server from root dir
            },
            port: 8000,
            ui: {
              port: 8080,
              weinre: {
                port: 9090
              }
            },
            open: false
          }
        },

    //  Uglify
    uglify: {
      options: {
        // Use these options when debugging
        mangle: false,
        compress: false,
        // beautify: true

      },
      dist: {
        files: {
          'js/materialize.min.js': 'js/materialize.js',
          'js/plugins.min.js': 'js/plugins.js',
          'js/custom-script.min.js': 'js/custom-script.js',
        }
      }
    },
    
    //Replace min css
    replace: {
      min: {
      src: ['html/**/*.html'],
      dest: 'dist/',
      replacements: [{
        from: '/materialize.css',
        to: '/materialize.min.css'
      },{
        from: '/style.css',                   
        to: '/style.min.css'
      },{
        from: '/custom.css',                   
        to: '/custom.min.css'
      },{
        from: '/materialize.js',                   
        to: '/materialize.min.js'
      },{
        from: '/plugins.js',                   
        to: '/plugins.min.js'
      }]
    }
  },

    //Clean folder 
    clean: {
      dist: {
       src: [ 'dist/' ]
     },
     temp: {
       src: [ 'temp/' ]
     },
   },


    //Watch for any files changes
    watch: {
      sass: {
        files: ['sass/**/*'],
        tasks: ['sass-compile'],
        options: {
          interrupt: false,
          spawn: false,
        },
      }
    },

    prettify: {
      options: {
        "indent": 2,
        "indent_char": " ",
        "indent_scripts": "normal",
        "wrap_line_length": 0,
        "brace_style": "collapse",
        "preserve_newlines": true,
        "max_preserve_newlines": 1,
        "unformatted": [
          "a",
          "code",
          "pre"
        ]
      },      
      // Prettify a directory of files 
      all: {
        expand: true,
        cwd: 'html/',
        ext: '.html',
        src: ['**/*.html'],
        dest: 'html/'
      },
    },


    //Concurrent
    concurrent: {
      options: {
        logConcurrentOutput: true,
        limit: 10,
      },
      monitor: {
        tasks: ["watch:sass", "notify:watching", 'server']
      },
    },


    //Notifications for task complition
    notify: {
      watching: {
        options: {
          enabled: true,
          message: 'Watching Files!',
          title: "Materialize Admin",
          success: true,
          duration: 1
        }
      },

      css: {
        options: {
          enabled: true,
          message: 'Sass Compiled!',
          title: "Materialize Admin",
          success: true,
          duration: 1
        }
      },

      js: {
        options: {
          enabled: true,
          message: 'JS Compiled!',
          title: "Materialize Admin",
          success: true,
          duration: 1
        }
      },

      server: {
        options: {
          enabled: true,
          message: 'Server Running!',
          title: "Materialize Admin",
          success: true,
          duration: 1
        }
      }
    },

  });

  // load the tasks  
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-clean');  
  grunt.loadNpmTasks('grunt-concurrent');
  grunt.loadNpmTasks('grunt-notify');
  grunt.loadNpmTasks('grunt-text-replace');  
  grunt.loadNpmTasks('grunt-browser-sync');  
  grunt.loadNpmTasks('grunt-postcss');
  grunt.loadNpmTasks('grunt-prettify');

  // define the tasks
  grunt.registerTask(
    'dist',[
    'clean:dist',
    'dist-css',
    'dist-js',
    'copy',
    'replace:min',
    ]);
  
  grunt.registerTask('sass-compile', ['sass:main', 'notify:css']);
  grunt.registerTask('dist-css', ['sass-compile', 'postcss:main', 'sass:dist', 'notify:css']);

  grunt.registerTask('dist-js', ['uglify:dist', 'notify:js']);

  grunt.registerTask('server', ['browserSync', 'notify:server']);
  grunt.registerTask("monitor", ["concurrent:monitor"]);
};



require.config({
    paths: {
        // Common libs
        jquery: 'libs/jquery',
        backbone: 'libs/backbone',
        underscore: 'libs/underscore',
        // datamap libs and custom code
        d3: '../datamaps/js/libs/d3/d3.v3.min',
        topojson: '../datamaps/js/libs/topojson/topojson.v1.min',
        datamaps: 'libs/datamaps',
        // Scribbler libs and custom code
        codemirror: '../scribbler/libs/codemirror/lib/codemirror',
        jsmode: '../scribbler/libs/codemirror/mode/javascript/javascript',
        cssmode: '../scribbler/libs/codemirror/mode/css/css',
        xmlmode: '../scribbler/libs/codemirror/mode/xml/xml',
        htmlmode: '../scribbler/libs/codemirror/mode/htmlmixed/htmlmixed',
        simplehint: '../scribbler/libs/codemirror/addon/hint/simple-hint',
        scribblereditor: '../scribbler/js/scribbler-editor',
        scribblermenu: '../scribbler/js/scribbler-menu',
        djangohint: '../scribbler/js/djangohint'
    },
    shim: {
        codemirror: {
            exports: 'CodeMirror'
        },
        simplehint: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        },
        jsmode: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        },
        cssmode: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        },
        xmlmode: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        },
        htmlmode: {
            exports: 'CodeMirror',
            deps: ['xmlmode', 'jsmode', 'cssmode']
        },
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        underscore: {
            exports: '_'
        },
        datamaps: {
            deps: ['d3', 'topojson'],
            exports: "Datamap"
        },
        topojson: {
            deps: ['d3'],
            exports: 'topojson'
        },
        d3: {
            exports: 'd3'
        }
    }
});

require([
    'scribblerMain',
    'mapMain'
], function (scribblerMain, HomeMap) {
    scribblerMain.initialize()
    HomeMap.initialize()

})
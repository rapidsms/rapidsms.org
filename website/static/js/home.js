
require.config({
    paths: {
        // Common libs
        jquery: 'libs/jquery',
        backbone: 'libs/backbone',
        underscore: 'libs/underscore',
        // datamap libs and custom code
        d3: 'libs/d3',
        datamap: 'libs/datamaps-all-stripped',
        homemap: 'homemap_config',
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
        d3: {
            exports: 'd3'
        },
    }
});

require(['jquery', 'scribblereditor', 'scribblermenu'], function ($, ScribbleEditor, ScribbleMenu) {
    'use strict';
    // Load scribbler's dependencies and plugins and render scribbler

    var pluginlist = [],
        script;

    $.noConflict(true);

    // Dynamically loads additional plugins for django-scribbler
    function pluginLoader(name, editor, menu) {
        var path = "./plugins/" + name;
        require([path], function (plugin) {
            plugin.call(null, editor, menu);
        });
    }

    script = $("script[data-scribbler-plugins]");

    if (script.length) {
        pluginlist = script.data("scribblerPlugins").split(",");
    }

    $(document).ready(function () {
        var editor = new ScribbleEditor(),
            menu = new ScribbleMenu();
        editor.bind("open", menu.close, menu);
        function executePlugin(name) {
            pluginLoader(name, editor, menu);
        }
        pluginlist.map(executePlugin);
        editor.render();
        menu.render();
    });
});

require(['homemap_config', 'homemap_data'], function (HomeMap, homemap_data) {
    // Load dependencies for the map on the homepage.
    // Once homemap_data is provided, initialize the map and render it
    var home_map = HomeMap.init(homemap_data);
    home_map.render();
});

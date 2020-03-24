define(['jquery', 'scribblereditor', 'scribblermenu'], function ($, ScribbleEditor, ScribbleMenu) {
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

    var initialize = function(){
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
    }

    return {
        initialize: initialize
    }
});
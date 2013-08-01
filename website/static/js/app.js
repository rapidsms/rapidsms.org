define([
    'jquery',
    'underscore',
    'd3',
    'scribblerMain',
    'mapMain'
], function ($, _, d3, scribblerMain, HomeMap) {

    var initialize = function(){
        scribblerMain.initialize()
        HomeMap.initialize()
    }

    return {
        initialize: initialize
    }
})
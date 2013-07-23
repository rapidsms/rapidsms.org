define(['jquery', 'underscore', 'backbone', 'd3', 'topojson', 'datamaps'],
    function ($, _, Backbone, d3, topojson, Datamap) {
        return {
            draw: function(){
                var map = this.map
                return map.draw()
            },
            bubbles: function(bubbles){
                var map = this.draw()
                return map.bubbles(bubbles, {
                    popupTemplate:function (geography, data) {
                        var node = '<div class="hoverinfo">' +
                           '<% if (data.name) { %> <strong><%= data.name %></strong><% } %>' +
                           '<br/>' +
                           '<% if (data.description) { %> Started in <%= data.description %><br/> <% } %>' +
                           '<%= data.country %>' +
                           '</div>';
                        return _.template(node, {'data': data})
                    }
                });
            },
            init: function(scope, data, fills, element) {
                this.map = new Datamap({
                    element: element,
                    scope: 'world',
                    geographyConfig: {
                        hideAntarctica: false,
                        popupOnHover: true,
                        highlightOnHover: false
                    },
                    setProjection: function(element, options) {
                        var projection, path;
                        projection = d3.geo[options.projection]()
                          .scale(element.offsetWidth * scope.scale)
                          .translate([element.offsetWidth / 2, element.offsetHeight / 1.8])
                          .center([scope.lon, scope.lat]);
                        path = d3.geo.path()
                            .projection( projection );

                        return {path: path, projection: projection};
                    },
                    fills: fills,
                    data: data
                });
                return this
            }
    };
});
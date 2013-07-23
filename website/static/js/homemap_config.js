define(['jquery', 'underscore', 'd3', 'topojson', 'datamaps'],
    function ($, _, d3, topojson, Datamap) {
        return {
            draw: function(){
                var map = this.map
                map.draw()
                return map
            },
            bubbles: function(bubbles){
                var map = this.draw()
                map.bubbles(bubbles, {
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

                // hack to bind to a onclick event
                this.map.svg.selectAll(".datamaps-bubble").on('click', function(){
                    data = JSON.parse(this.dataset.info)
                    window.location = data.url
                })
                return this
            },
            init: function(scope, data, fills, element) {
                this.map = new Datamap({
                    element: document.getElementById(element),
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
                        path = d3.geo.path().projection( projection );
                        return {path: path, projection: projection};
                    },
                    fills: fills,
                    data: data,

                });

                return this
            }
    };
});
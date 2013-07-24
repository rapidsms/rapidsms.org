define(['jquery', 'underscore', 'd3', 'topojson', 'datamaps'],
    function ($, _, d3, topojson, Datamap) {
        return {
            draw: function(){
                var map = this.map
                map.draw()
                return this
            },
            init: function(scope, data, fills, element) {

                var node = '<div class="hoverinfo">' +
                   '<% if (data.name) { %> <strong><%= data.name %></strong><% } %>' +
                   '<br/>' +
                   '<% if (data.description) { %> Started in <%= data.description %><br/> <% } %>' +
                   '<%= data.country %>' +
                   '</div>';

                this.map = new Datamap({
                    element: document.getElementById(element),
                    scope: 'world',
                    geographyConfig: {
                        hideAntarctica: false,
                        popupOnHover: true,
                        highlightOnHover: false,
                        popupTemplate: function (geography, data) {
                            if (data){
                                var node = '<div class="hoverinfo">' +
                                   '<strong><%= data.name %> in <%= data.country %> </strong>' +
                                   '<br/>' +
                                   '<% if (data.description) { %> <%= data.description %>...<br/> <% } %>' +

                                   '</div>';
                                return _.template(node, {'data': data})
                            }
                        }
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
                    done: function(datamap) {
                        datamap.svg.selectAll('.datamaps-subunit').on('click', function(geography) {
                            var data = datamap.options.data
                            var country_code = geography.id
                            var country = datamap.options.data[country_code]
                            if (country){
                                window.location = country.url
                            }
                        });
                    }
                });

                return this
            }
    };
});
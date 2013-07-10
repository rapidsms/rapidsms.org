define(['jquery', 'underscore', 'backbone', 'd3', 'datamap'], function ($, _, Backbone, d3) {
    return {
        init: function(data) {
            return new Map({
                scope: 'usa',
                el: $('#home-map'),
                geography_config: {
                    highlightBorderColor: '#222',
                    highlightOnHover: true,
                    popupTemplate: _.template(
                        '<div class="hoverinfo"><strong><%= geography.properties.name %></strong> <% if (data.electoralVotes) { %><hr/>  Electoral Votes: <%= data.electoralVotes %> <% } %></div>'
                    )
                },
                fills: {
                    'REP': '#CC4731',
                    'DEM': '#306596',
                    'HEAVY_DEM': '#667FAF',
                    'LIGHT_DEM': '#A9C0DE',
                    'HEAVY_REP': '#CA5E5B',
                    'LIGHT_REP': '#EAA9A8',
                    defaultFill: '#EDDC4E'
                },
                data: data
            });
        }
    };
});

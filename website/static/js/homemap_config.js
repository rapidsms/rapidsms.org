define(['jquery', 'underscore', 'backbone', 'd3', 'datamap'], function ($, _, Backbone, d3) {
    return {
        init: function(data) {
            return new Map({
                scope: 'world',
                el: $('#home-map'),
                geography_config: {
                    highlightBorderColor: '#222',
                    highlightOnHover: true,
                    popupTemplate: _.template(
                       '<div class="hoverinfo">',
                       '<% if (data.name) { %> <strong><%= data.name %></strong><br/><% } %>',
                       '<% if (data.description) { %>',
                       'Started in <%= data.description %><br/> <% } %>',
                       '<%= geography.properties.name %>',
                       '</div>'
                    )
                },

                fills: {
                    project: 'green',
                    defaultFill: '#EDDC4E'
                },
                data: data
            });
        }
    };
});

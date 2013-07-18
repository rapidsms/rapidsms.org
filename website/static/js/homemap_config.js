define(['jquery', 'underscore', 'backbone', 'd3', 'datamap'], function ($, _, Backbone, d3) {
    return {
        init: function(data) {
            var node = '<div class="hoverinfo">' +
                       '<% if (data.name) { %> <strong><%= data.name %></strong><br/><% } %>' +
                       '<% if (data.description) { %> Started in <%= data.description %><br/> <% } %>' +
                       '<%= geography.properties.name %>' +
                       '</div>';
            return new Map({
                // restore scope: 'world'
                // scope: 'africa',
                scope: 'world',
                el: $('#home-map'),
                geography_config: {
                    highlightBorderColor: '#333333',
                    highlightOnHover: true,
                    popupTemplate: _.template(node)
                },

                fills: {
                    'project': 'green',
                    defaultFill: '#CCCCCC'
                },
                data: data
            });
        }
    };
});

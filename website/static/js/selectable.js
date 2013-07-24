/* Used in conjunction with django-selectable to override some of the
   defaults and use Bootstrap styles. */

(function($){
    $.ui.djselectable.prototype._initDeck = function() {
        // Use a custom div to hold selected items, and append it after the field.
        var self = this;
        self.deck = $("<div>").addClass("span6 selections");
        console.log(self.element);
        $(self.element).parent().append(self.deck);
        $(self.hiddenMultipleSelector).each(function (i, input) {
            self._addDeckItem(input);
        });
    };

    $.ui.djselectable.prototype._addDeckItem = function(input) {
        // Add new deck list item from a given hidden input.
        var self = this,
            label = $('<span>').addClass('label'),
            item = {element: self.element, input: input, wrapper: label, deck: self.deck},
            button;
        label.html($(input).attr('title') + " ");
        if (self._trigger("add", null, item) === false) {
            input.remove();
        } else {
            button = this._removeButtonTemplate(item);
            button.click(function (e) {
                e.preventDefault();
                if (self._trigger("remove", e, item) !== false) {
                    $(input).remove();
                    label.remove();
                }
            });
            label.append(button).appendTo(this.deck);
        }
    };

    $.ui.djselectable.prototype._removeButtonTemplate = function(item) {
        // Use a Bootstrap icon.
        var icon = $("<i>").addClass("icon-white icon-remove");
        var button = $("<a>").attr("href", "").append(icon);
        return button;
    };
})(jQuery);
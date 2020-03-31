(function($){
    $('#id_email').bind('keyup blur', function() {
        $('#id_gravatar_email').val($(this).val());
    });
})(jQuery);
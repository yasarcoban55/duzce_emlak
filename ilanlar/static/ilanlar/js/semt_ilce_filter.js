window.addEventListener('load', function() {
    (function($) {
        $('#id_il').change(function() {
            var ilId = $(this).val();
            var ilceSelect = $('#id_ilce');
            ilceSelect.html('<option value="">---------</option>');
            if (!ilId) return;
            $.get('/admin/ajax/ilce-list/', { il_id: ilId }, function(data) {
                $.each(data.ilceler, function(i, ilce) {
                    ilceSelect.append($('<option>', {
                        value: ilce.id,
                        text: ilce.ad
                    }));
                });
            });
        });
    })(django.jQuery);
});
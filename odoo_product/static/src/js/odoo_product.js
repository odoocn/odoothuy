$(document).ready(function () {
        /* ----- COMPARE STUFF ---- */
	$(document).on('click','.js_flag_compare .js_compare_btn', function () {        	
            var $data = $(this).parents(".js_flag_compare:first");        
            var self=this;
            f=openerp.jsonRpc($data.data('controller') || '/flag_compare', 'call', {'id': +$data.data('id'), 'object': $data.data('object')})
            f
                .then(function (result) {
                    $data.toggleClass("css_unpublished css_published");
                    $data.parents("[flag-compare]").attr("flag-compare", +result ? 'on' : 'off');
                }).fail(function (err, data) {
                    alert(err);
                });
        });
    });

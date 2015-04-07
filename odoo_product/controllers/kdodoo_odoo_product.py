# -*- coding: utf-8 -*-
from openerp import http

from openerp.addons.web.controllers import main


class kdodoo_website(http.Controller):
    @http.route('/products', auth='public', website=True)
    def index(self):
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context

#         Data = registry['ir.model.data']
#         _, ta_group_id = Data.get_object_reference(cr, uid, 'odoo_product', 'kdodoo_product_website')
        kop_obj = registry['kdodoo.website.product']
        pros_ids = kop_obj.search(
            http.request.cr, http.request.uid,[],
            context=http.request.context)
        pros = kop_obj.browse(cr, uid, pros_ids)
        return http.request.website.render('odoo_product.index', {
            'pros': pros,
        })
    
    @http.route('/pros/<model("kdodoo.website.product"):pro>/', auth='public', website=True)
    def pro(self, pro):
        return http.request.website.render('odoo_product.pro', {
            'pro': pro,
        })
    
    @http.route(['/flag_compare'], type='json', auth="public", website=True)
    def action_flag_compare(self, id, object):
        _id = int(id)
        registry = http.request.registry
        _object = registry[object]
        obj = _object.browse(http.request.cr, http.request.uid, _id)

        values = {}
        if 'flag_compare' in _object._all_columns:
            values['flag_compare'] = not obj.flag_compare
        _object.write(http.request.cr, http.request.uid, [_id],
                      values, context=http.request.context)

        obj = _object.browse(http.request.cr, http.request.uid, _id)
        return bool(obj.flag_compare)
    
from openerp.osv import orm, fields


class kdodoo_website_product(orm.Model):
    _name = 'kdodoo.website.product'
    _inherit = 'product.product'
    
    _columns= {
               'website_published':fields.boolean('Publish?'),
               'flag_compare':fields.boolean('Flag Compare')
               }
    
    def img(self, cr, uid, ids, field='image_small', context=None):
        return "/website/image?model=%s&field=%s&id=%s" % (self._name, field, ids[0])
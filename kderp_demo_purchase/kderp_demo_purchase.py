from openerp.osv import fields, osv
class purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _description = 'Kderp Demo Purchase Order'
    _columns = {
               'code' : fields.char("Code"),
                }
purchase_order()

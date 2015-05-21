from openerp.osv import fields, osv
class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = ['mail.thread','account.invoice']
    _description = 'Client Payment'
    _columns = {
               'code' : fields.char("Code"),
                }
account_invoice()

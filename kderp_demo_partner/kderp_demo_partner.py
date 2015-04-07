from openerp.osv.orm import Model
from openerp.osv import fields, osv

import openerp.addons.decimal_precision as dp
import re

class res_partner(Model):
    _inherit = 'res.partner'
    _description = 'Demo Partner'

    _columns = {
                'code':fields.char('Code'),
                }

res_partner()

import re
import time

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools import float_round, float_is_zero, float_compare
from openerp.tools.translate import _

class res_currency(osv.osv):
    _name = "res.currency"
    _description = "Currency"
    _inherit = "res.currency"
    
    _sql_constraints=[('kderp_currency_unique','unique(name)','Currency must be unique !')]
            
    _columns={
              'pattern':fields.char("Pattern",size=32)
              }
    _defaults={
               'pattern':lambda *a:"#,##0.00"
               }
res_currency()
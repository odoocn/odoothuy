from openerp.osv.orm import Model
from openerp.osv import fields, osv

import openerp.addons.decimal_precision as dp
import re

class demo_contract_cur(Model):
    _name = 'demo.contract.cur'
    _description = 'Demo Contract Currency'

    _columns = {
                
                'name': fields.many2one('res.currency','Currency'),
                'rate': fields.float('Ex. Rate', digits = (12,2),),
                'rounding':fields.float('Rounding', digits =(12,2)),
                'default_curr': fields.boolean('Default'),        
                'contract_id':fields.many2one('demo.contract','Contract'),
        }
    _defaults={
               'default_curr':True
               }
demo_contract_cur()
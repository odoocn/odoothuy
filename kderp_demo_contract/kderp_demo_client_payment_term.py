from openerp.osv.orm import Model
from openerp.osv import fields, osv

import openerp.addons.decimal_precision as dp
import re

class demo_client_payment_term(Model):
    _name = 'demo.client.payment.term'
    _description = 'Demo Client Payment Term'

    _columns = {
                
                'name': fields.char('Description'),
                'sequence': fields.integer('Sequence'),
                'type':fields.selection([('adv','Advance Payment'),('p','Progress'),('re','Retention')],'Type'),
                'value': fields.selection([('percent', 'Percent'),('fixed', 'Fixed Amount')], 'Value'),
                'value_amount':fields.float('Percentage', help="For Value percent enter % ratio between 0-1."),
                'due_date':fields.date('Due date'),
                'tax_include':fields.boolean('Included VAT'),        
                'contract_id': fields.many2one('demo.contract', 'Contract'),
        }
demo_client_payment_term()
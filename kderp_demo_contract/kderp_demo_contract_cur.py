from openerp.osv.orm import Model
from openerp.osv import fields, osv

import openerp.addons.decimal_precision as dp
import re

class demo_contract_cur(Model):
    _name = 'demo.contract.cur'
    _description = 'Demo Contract Currency'
    _order = 'default_curr desc'
    
    def create_currency(self, cr, uid, contract_id, context={}):
        if not context: context={}
        cur_obj = self.pool.get('res.currency')
        cur_ids = cur_obj.search(cr, uid, [('id','>',0)])
        new_id = False
        new_ids = []
        for cur in cur_obj.browse(cr, uid, cur_ids):
            if cur.name == "USD":
                new_id = self.create(cr, uid, {'name':cur.id, 'rate':cur.rate, 'rounding':cur.rounding, 'default_curr':False, 'contract_id':contract_id})
                new_ids.append(new_id)
            elif cur.name == "VND":
                new_id = self.create(cr, uid, {'name':cur.id, 'rate':cur.rate, 'rounding':cur.rounding, 'default_curr':True, 'contract_id':contract_id})
                new_ids.append(new_id)
        return new_ids
    _columns = {
                
                'name': fields.many2one('res.currency','Currency'),
                'rate': fields.float('Ex. Rate', digits = (12,2),),
                'rounding':fields.float('Rounding', digits =(12,2)),
                'default_curr': fields.boolean('Default'),        
                'contract_id':fields.many2one('demo.contract','Contract'),
        }
    _defaults={
               
               }
demo_contract_cur()
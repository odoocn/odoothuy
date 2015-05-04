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
    
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        unlink_ids = []

        for kccur in self.browse(cr, uid, ids):
            if kccur.default_curr:
                raise osv.except_osv("KDERP Warning","""You cannot delete an Contract Currency is Default, Please follow steps:
                                                            1. Click Discard Button.
                                                            2. Click Edit -> Uncheck default Currency, 
                                                            3. Click Save.
                                                            4. Delete Contract Currency Again !""")
            else:
                unlink_ids.append(kccur.id)

        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True
    
    _columns = {
                
                'name': fields.many2one('res.currency','Currency'),
                'rate': fields.float('Ex. Rate', digits = (12,2),),
                'rounding':fields.float('Rounding', digits =(12,2)),
                'default_curr': fields.boolean('Default'),        
                'contract_id':fields.many2one('demo.contract','Contract'),
                'tax_id': fields.many2many('account.tax', 'kderp_contract_tax', 'contract_currency_id', 'tax_id', 'VAT (%)', domain="[('parent_id','=',False),('type_tax_use','=','sale')]",change_default=True),
                'amount':fields.float('Amount'),
                'amount_tax':fields.float('Amount Tax'),
                'amount_total':fields.float('Total')
        }

    _defaults={
               
               }
demo_contract_cur()
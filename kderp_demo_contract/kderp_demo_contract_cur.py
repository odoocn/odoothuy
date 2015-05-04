from openerp.osv.orm import Model
from openerp.osv import fields, osv

import openerp.addons.decimal_precision as dp
import re
from openerp.tools import float_round

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
    
    def _get_quotation_lists(self, cr, uid, ids, name, arg, context=None):
        res = {}
        contract_ids=",".join(map(str,ids)) 
        cr.execute("""
                    SELECT 
                        dcc.id,
                        trim(array_to_string(array_agg(so.id::text),' '))
                    FROM 
                        demo_contract_cur dcc 
                    left join
                        demo_contract dc on dcc.contract_id = dc.id and dcc.default_curr = true
                    left join
                        sale_order so on dc.id=so.contract_id
                    where dcc.id in (%s)
                    group by
                        dcc.id
                    """%(contract_ids))
        for contract_id, list_id in cr.fetchall():
            tmp_list = list_id
            if not tmp_list:
                tmp_list=[]
            elif tmp_list.isdigit():
                tmp_list=[int(tmp_list)]
            else:
                tmp_list=list(eval(tmp_list.strip().replace(' ',',').replace(' ','')))
            res[contract_id]=tmp_list
        return res
    
    def _get_summary_amount(self, cr, uid, ids, name, arg, context=None):
        res={}
        var = self.browse(cr, uid, ids, context)
        amount=0
        amount_tax = 0
        amount_total = 0
        for dcc in var:
            res[dcc.id]={'amount' : 0,
                         'amount_tax':0,
                         'amount_total':0
                        }
            for so in dcc.quotation_lists:
                if so.state not in ('draft', 'cancel'):                                        
                    for qsl in so.quotation_submit_line:
                        if qsl.currency_id.name == 'VND' and dcc.name.name=='VND':
                            approved_amount_e = so.approved_amount_e
                            approved_amount_m = so.approved_amount_m
                        elif qsl.currency_id.name != 'VND' and dcc.name.name!='VND':
                            approved_amount_e = so.approved_amount_e
                            approved_amount_m = so.approved_amount_m
                        elif qsl.currency_id.name != 'VND' and dcc.name.name=='VND':
                            approved_amount_e = so.approved_amount_e*qsl.currency_id.rate_silent
                            approved_amount_m = so.approved_amount_m*qsl.currency_id.rate_silent
                        elif qsl.currency_id.name == 'VND' and dcc.name.name!='VND':
                            approved_amount_e = so.approved_amount_e/dcc.rate
                            approved_amount_m = so.approved_amount_m/dcc.rate
 
                        amount += (approved_amount_e+approved_amount_m)
                        
                    res[dcc.id]={'amount' : amount,
                                 'amount_tax':amount*dcc.tax_id.amount,
                                 'amount_total':amount+amount*dcc.tax_id.amount}
        return res
    _columns = {
                
                'name': fields.many2one('res.currency','Currency'),
                'rate': fields.float('Ex. Rate', digits = (12,2),),
                'rounding':fields.float('Rounding', digits =(12,2)),
                'default_curr': fields.boolean('Default'),        
                'contract_id':fields.many2one('demo.contract','Contract'),
                'tax_id': fields.many2many('account.tax', 'kderp_contract_tax', 'contract_currency_id', 'tax_id', 'VAT (%)', domain="[('parent_id','=',False),('type_tax_use','=','sale')]",change_default=True),
                'amount':fields.function(_get_summary_amount,string='Amount',type='float', digits_compute=dp.get_precision('Amount'),multi='_multi_get_summary'),
                'amount_tax':fields.function(_get_summary_amount,string='VAT',type='float', digits_compute=dp.get_precision('Amount'),multi='_multi_get_summary'),
                'amount_total':fields.function(_get_summary_amount,string='Total',type='float', digits_compute=dp.get_precision('Amount'),multi='_multi_get_summary'),
                'quotation_lists':fields.function(_get_quotation_lists, relation='sale.order',type='one2many',string='Quotations List',method=True),
        }

    _defaults={
               
               }
demo_contract_cur()
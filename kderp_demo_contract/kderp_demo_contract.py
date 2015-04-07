from openerp.osv.orm import Model
from openerp.osv import fields, osv

import openerp.addons.decimal_precision as dp
import re

class demo_contract(Model):
    _name = 'demo.contract'
    _description = 'Demo Contract'
    _rec_name="code"
    
    def onchange_partner_id(self, cr, uid, ids, partner_id):
            partner = self.pool.get('res.partner')
            if not partner_id:
                return {'value': {
                    'fiscal_position': False,
                    'payment_term_id': False,
                    }}
            supplier_address = partner.address_get(cr, uid, [partner_id], ['default'])
            supplier = partner.browse(cr, uid, partner_id)
            return {'value': {
                'pricelist_id': supplier.property_product_pricelist_purchase.id,
                'fiscal_position': supplier.property_account_position and supplier.property_account_position.id or False,
                'payment_term_id': supplier.property_supplier_payment_term.id or False,
                'client_id': supplier.street or False,
                'invoice_id': supplier.street or False,
                }}
        
    _columns = {
       'code': fields.char('Code', required=True),
       'name':fields.char('Description', required=True),
       #
        'date':fields.date('Date of Contract'),
        'project_name':fields.char('Prj. Name'),
        'contract_ref':fields.char('Contract Ref.'),
        'client_representative_name': fields.char('Representative'),
        #
        'owner':fields.many2one('res.partner','Owner', select=2, ondelete='restrict'),
        'partner_id':fields.many2one('res.partner', 'Client'),
        #'client_id':fields.many2one('res.partner','Address'),
        'client_id':fields.char('Address'),
        #'invoice_id':fields.many2one('res.partner', 'Invoice Address'),
        'invoice_id':fields.char('Invoice Address'),
        'location_id':fields.many2one('kderp.demo.location','Location'),
        
        #
        'registration_date':fields.date('Reg. Date'),
        'started_date':fields.date('Start Date'),
        'completion_date':fields.date('Comp. Date'),
        'closed_date':fields.date('Close Date'),
        'outstanding':fields.selection([('none','None'),('bc_check','BC Check'),('pm_check','PM Check')],"Outstanding",select=1),
        'attached_contract_sent':fields.boolean('Contract Sent '),
        'attached_contract_received':fields.boolean('Contract Received '),
        'attached_approved_quotation':fields.boolean('Approved Quotation'),
        #
        'demo_payment_term_ids':fields.one2many('demo.client.payment.term','contract_id','Payment Term'),
        'demo_contract_cur_ids':fields.one2many('demo.contract.cur','contract_id','Contract Cur.'),
        'demo_contract_summary_cur_ids':fields.one2many('demo.contract.cur','contract_id', string = 'Cur.', domain=[('default_curr','=',True)]),
        }
    _defaults={
               'outstanding':'none'
               }

demo_contract()
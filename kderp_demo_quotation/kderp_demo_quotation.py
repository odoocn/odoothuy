from openerp.osv.orm import Model
from openerp.osv import fields, osv

import openerp.addons.decimal_precision as dp
import re

class demo_contract(osv.osv):
    _inherit = 'demo.contract'
    _columns = {
        'quotation_ids': fields.one2many('sale.order','contract_id',)
    }
    _defaults = {}   
demo_contract()

class sale_order(Model):
    _inherit = 'sale.order'
    _description = 'Demo Quotation'
    
    STATE_SELECTION=[('draft', 'Not yet decided'),
                    ('done', 'Work Received'),
                    ('cancel', 'Cancelled')]
    #defined
    def _get_newcode(self,cr,uid,context={}):
        cr.execute("""Select 
                        prefix ||
                        substring(date_part('year',current_date)::text from 3 for 2) || '-' ||
                        lpad(coalesce(max((substring(so.name from length(prefix)+4 for padding))::int)+1,1)::text,padding,'0') ||
                        '-' || suffix
                    from 
                        ir_sequence cis
                    left join
                        sale_order so on so.name ilike cis.prefix || substring(date_part('year',current_date)::text from 3 for 2) || '-' || lpad('_',padding,'_') || '%%'  
                    where 
                        (cis.code ilike 'kderp_hanoi_quotation') and active=True
                    group by
                        cis.id""")
        new_code=False
        res = cr.fetchone()
        if res:
            new_code = res[0]
        return new_code
    
    def _get_approved_amount_currency(self, cr, uid, ids,  name, args, context=None):
        res={}
        for kdq in self.browse(cr, uid, ids):
            res[kdq.id]={'currency':False}
            for kdsq in kdq.quotation_submit_line:
                res[kdq.id]['currency']=kdsq.currency_id.id
        return res
    
    def _get_currency_from_quotation_submit_line(self, cr, uid, ids, context=None):
        res=[]
        for kdq in self.pool.get('kderp.demo.sale.order.submit.line').browse(cr, uid, ids, context=context):
            res.append(kdq.order_id.id)
        return res
    
    def _get_approved_amount_info(self, cr, uid, ids, name, args, context=None):
        res={}
        for kdq in self.browse(cr, uid, ids):
            res[kdq.id]={'approved_amount_e':0,
                         'approved_amount_m':0,
                         'approved_amount_total':0}
            for a in kdq.sale_order_line:
                res[kdq.id]['approved_amount_e']=a.price_unit+a.discount
                res[kdq.id]['approved_amount_total']=a.price_unit+a.discount
            for a in kdq.sale_order_line_m:
                res[kdq.id]['approved_amount_m']=a.price_unit+a.discount
                res[kdq.id]['approved_amount_total']+=a.price_unit+a.discount
        return res
    
    def _get_approved_from_quotation_breakdown(self, cr, uid, ids, context=None):
        res = []
        for a in self.pool.get('kderp.demo.quotation.breakdown').browse(cr, uid, ids, context=context):
            res.append(a.order_id.id)
        return res
    
    _defaults={
                'company_id':'',
                'name': _get_newcode,
                'date_order': lambda *x: False,
               }
    _columns = {
       'name': fields.char('Quotation No.', size=16,required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, select=True),
       'dateofregistration':fields.date('Date of Registration'),
       'state': fields.selection(STATE_SELECTION, 'Status', readonly=1, select=1),
       #Client Info
       'partner_id':fields.many2one('res.partner', 'Client', required=0),
       'partner_address_id': fields.char('Address'),
       'partner_invoice_id': fields.char('Invoice Address'),
       'completion_date':fields.date('Completion Date'),
       'contract_id':fields.many2one('demo.contract', 'Contract'),
       'completion_date_contract':fields.date('Comp. Date of Contract'),
       #Quotation Info
       'owner':fields.many2one('res.partner','Owner', select=2, ondelete='restrict'),
       'location':fields.char('Location'),
       'project_name':fields.char('Project Name'),
       'register_by':fields.many2one('hr.employee', 'Registered By',select=2,ondelete='restrict'),
       'est_e_j':fields.many2one('hr.employee', 'Est. E.(J)', select=2, ondelete='restrict'),
       'est_e_v':fields.many2one('hr.employee', 'Est. E.(V)', select=2, ondelete='restrict'),
       'est_m_j':fields.many2one('hr.employee', 'Est. M.(J)', select=2, ondelete='restrict'),
       'est_m_v':fields.many2one('hr.employee', 'Est. M.(V)', select=2, ondelete='restrict'),
       'prj_manager_e':fields.many2one('hr.employee', 'Prj. Manager E.', select=2, ondelete='restrict'),
       'prj_manager_m':fields.many2one('hr.employee', 'Prj. Manager M.', select=2, ondelete='restrict'),
       'site_manager_e':fields.many2one('hr.employee', 'Site Manager E.', select=2, ondelete='restrict'),
       'site_manager_m':fields.many2one('hr.employee', 'Site Manager M.', select=2, ondelete='restrict'),
       'description':fields.text('Desc.'),
       'remarks':fields.text('Remarks'),
       #Quotation Attachment Info
       'q_attached':fields.boolean('Quotation'),    
       'q_attached_be':fields.boolean('Q.Budget Electrical'),
       'q_attached_bm':fields.boolean('Q.Budget Mechanical'),
       'q_attached_qcombine':fields.boolean('Q.Budget Combine'),
       'q_budget_na':fields.boolean('N/A'),
       #Quotation Submit info
       'quotation_type':fields.selection([('E','Electrical'),('M','Mechenical'),('E/M','Electrical & Mechenical')], 'Quotation Type'),
       'date_order':fields.date('Date of Submit'),
       'quotation_submit_line': fields.one2many('kderp.demo.sale.order.submit.line', 'order_id', 'Submit Lines', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True),
       #Job Info
       'sale_order_line': fields.one2many('kderp.demo.quotation.breakdown', 'order_id', 'Breakdown for Electrical',context={'job_type':'E'}, domain=[('job_type','=','E')]),
       'sale_order_line_m':fields.one2many('kderp.demo.quotation.breakdown','order_id','Breakdown for Mechanical',context={'job_type':'M'}, domain=[('job_type','=','M')]),
         
       'job_e_id':fields.many2one('account.analytic.account','Job. (E)'),
       'q_budget_no_e':fields.char('Budget No.',size=20),
       'q_exrate_e':fields.float("Ex.Rate"),
       'q_prj_budget_amount_e':fields.float("W.B. Amount (E)"),
       'budget_state_e':fields.char('Budget Status',size=10),
       'temp_percentage_e':fields.float('%',digits=(16,2)),
         
       'job_m_id':fields.many2one('account.analytic.account','Job. (M)'),
       'q_budget_no_m':fields.char('Budget No.',size=20),
       'q_exrate_m':fields.float("Ex.Rate"),
       'q_prj_budget_amount_m':fields.float("W.B. Amount  (M)"),
       'budget_state_m':fields.char('Budget Status',size=10),
       'temp_percentage_m':fields.float('%',digits=(16,2)),       
         
       'summary_quotation_ids':fields.one2many('kderp.demo.summary.of.quotation', 'order_id', 'Summary of Quotation', readonly=True),
        #Working Budget
        #'ir.attachment':(_get_attachement_link,['res_model','res_id','q_attached','q_attached_be','q_attached_bm','q_attached_qcombine','q_attached_je','q_attached_jm','q_attached_jcombine'],20)}),
        'q_attached_je':fields.boolean('J.Budget E.'),
        'q_attached_jm':fields.boolean('J.Budget M.'),
        'q_attached_jcombine':fields.boolean('J.Budget Combine'),
        'quotation_job_budget_na':fields.boolean('N/A'),
        'total_working_budget':fields.float('W.B.Amt.(M&E)'),
        #Show tree view
        'approved_amount_e':fields.function(_get_approved_amount_info, type='float', string='Approved E.', method=True,
                                             multi='_get_quotation_approved_info',digits_compute= dp.get_precision('Product Price'),
                                             store={'kderp.demo.quotation.breakdown':(_get_approved_from_quotation_breakdown, None, 35),
                                                    'sale.order':(lambda self, cr, uid, ids, c={}: ids, ['sale_order_line', 'sale_order_line_m'],10)
                                                    }),
        'approved_amount_m':fields.function(_get_approved_amount_info, type='float', string='Approved M.', method=True,
                                            multi='_get_quotation_approved_info',digits_compute= dp.get_precision('Product Price'),
                                            store={'kderp.demo.quotation.breakdown':(_get_approved_from_quotation_breakdown, None, 35),
                                                   'sale.order':(lambda self, cr, uid, ids, c={}: ids, ['sale_order_line', 'sale_order_line_m'],10)
                                                    }),
        'approved_amount_total':fields.function(_get_approved_amount_info, type='float',string='Total',method=True, 
                                                multi='_get_quotation_approved_info',digits_compute= dp.get_precision('Product Price'),
                                                store={'kderp.demo.quotation.breakdown':(_get_approved_from_quotation_breakdown, None, 35),
                                                       'sale.order':(lambda self, cr, uid, ids, c={}: ids, ['sale_order_line', 'sale_order_line_m'],10)
                                                    }),
        'currency':fields.function(_get_approved_amount_currency,method=True,type='many2one',relation='res.currency',size=16,string='Cur.',
                                    multi='_get_approved_amount_currency',
                                    store={'kderp.demo.sale.order.submit.line':(_get_currency_from_quotation_submit_line,None, 35),
                                           'sale.order':(lambda self, cr, uid, ids, c={}: ids, ['quotation_submit_line'],10)
                                           }),
       }
    
    # compute and search fields, in the same order that fields declaration
    
    # Constraints and onchanges
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        if not part:
            return {'value': {'partner_invoice_id': False, 'partner_shipping_id': False, 'partner_address_id': False,  'payment_term': False, 'fiscal_position': False}}

        part = self.pool.get('res.partner').browse(cr, uid, part, context={})
        #if the chosen partner is not a company and has a parent company, use the parent to choose the delivery, the 
        #invoicing addresses and all the fields related to the partner.
        if part.parent_id and not part.is_company:
            part = part.parent_id
        addr = self.pool.get('res.partner').address_get(cr, uid, [part.id], ['delivery', 'invoice', 'contact','default'])
        pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
        payment_term = part.property_payment_term and part.property_payment_term.id or False
        fiscal_position = part.property_account_position and part.property_account_position.id or False
        dedicated_salesman = part.user_id and part.user_id.id or uid

        val = {
            'partner_invoice_id': part.street,
            'partner_address_id': part.street,
            'partner_shipping_id': addr['delivery'],
            'payment_term': payment_term,
            'fiscal_position': fiscal_position,
            'user_id': dedicated_salesman,
        }
        if pricelist:
            val['pricelist_id'] = pricelist
        return {'value': val}

    _sql_constraints = [
        ('demo_quotation_name_uniq', 'unique(name)', 'Quotation No. must by unique'),]
    
    # CRUD methods
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order') or '/'
        r=self.pool.get('ir.rule').clear_cache(cr,uid)
        new_obj=super(sale_order, self).create(cr, uid, vals, context=context)
        return new_obj
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'name':'/',      
        })
        #raise osv.except_osv("E",default)
        res=super(sale_order, self).copy(cr, uid, id, default, context)
        self.write(cr, uid, [res], {'date_order':False})
        self.pool.get('ir.rule').clear_cache(cr,uid)
        return res
    
    # Action methods
    def action_work_received(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'done'}, context=context)
        return True
    
    def action_cancel(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True
    
    def action_cancel_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True
    
    def action_done_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True
    
sale_order()   
# 
class kderp_demo_sale_order_submit_line(Model):
    _name = "kderp.demo.sale.order.submit.line"
    _description = "Kderp Demo Sale Order Submit Line"
      
    def _get_amount_line(self, cr, uid, ids, name, args, context={}):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, line.amount, 1)
            vat_amount = cur_obj.round(cr, uid,line.currency_id, taxes['total_included']-line.amount)
            total = cur_obj.round(cr, uid,line.currency_id,taxes['total_included'])
            res[line.id]={'tax_amount':vat_amount,
                          'subtotal':total}
        return res
    _columns = {
        'order_id': fields.many2one('sale.order', 'Order', required=True, ondelete='cascade', select=True, readonly=True),
        'currency_id':fields.many2one('res.currency', 'Cur'),
        'name': fields.text('Description'),
        'amount':fields.float('Amount'),
        'tax_id': fields.many2many('account.tax', 'kderp_demo_sale_order_submit_tax', 'order_line_id', 'tax_id', 'Taxes'),
        'tax_amount':fields.function(_get_amount_line,type='float',string='VAT',method=True,multi='_get_amount_submit_line',digits_compute= dp.get_precision('Product Price'),
                                     store = {
                                              'kderp.demo.sale.order.submit.line':(lambda self, cr, uid, ids, c={}: ids, None, 5)}),
        'subtotal':fields.function(_get_amount_line,type='float',string='Sub-Total',method=True,multi='_get_amount_submit_line',digits_compute= dp.get_precision('Product Price'),
                                    store={'kderp.demo.sale.order.submit.line':(lambda self, cr, uid, ids, c={}: ids, None, 5)}),
            }                               
      
    def _get_tax_default(self,cr,uid,context):
        tax_ids = self.pool.get('account.tax').search(cr, uid,[('type_tax_use','=','sale'),('active','=',True),('id','=',10)])
        return tax_ids
      
    _defaults={
               'tax_id' : _get_tax_default
               }
kderp_demo_sale_order_submit_line()
  
class kderp_demo_quotation_breakdown(osv.osv):
    _name='kderp.demo.quotation.breakdown'    
    _description='Detail Quotation Breakdown'
    def _get_job_type(self,cr,uid,context={}):
        if not context:
            context={}
        return context.get('job_type',False)
      
    _columns={
                'name':fields.char('Description',size=250),
                'currency_id':fields.many2one('res.currency','Cur.',required=True),
                'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price')),
                'discount':fields.float('Discount',required=True),
                'order_id': fields.many2one('sale.order', 'Quotation', required=True, ondelete='restrict', select=True),
                'job_type':fields.selection([('E','Electrical'),('M','Mechanical')],'Type',required=True),
              }
    _sql_constraints=[('kderp_demo_breakdown_currency','unique(currency_id,order_id,job_type)','Currency for Temporary Breakdown must be unique !')]
    _order = 'order_id desc'
    _defaults = {
                 'discount':0.0,
                 'job_type':_get_job_type,
                 }
kderp_demo_quotation_breakdown()
  
class kderp_demo_summary_of_quotation(Model):
    _name = 'kderp.demo.summary.of.quotation'
    _description = 'KDERP Summary Of Quotation'
    _auto = False
    _columns={
              'currency_id':fields.many2one('res.currency','Cur.'),
              'amount':fields.float('Sub-Total'),
              'order_id':fields.many2one('sale.order','Order')
              }
    def init(self,cr):
        cr.execute("""Create or replace view kderp_demo_summary_of_quotation as
                      Select 
                            row_number() over (order by order_id,currency_id) as id,
                            sol.order_id,
                            currency_id,
                            sum(price_unit+discount) as amount
                      from 
                          kderp_demo_quotation_breakdown sol 
                      group by
                          order_id,currency_id""")
kderp_demo_summary_of_quotation()


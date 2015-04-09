from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class kderp_demo_budget_data(osv.osv):
    _name = 'kderp.demo.budget.data'
    _description = 'Budget Data for Job'
    
    def name_get(self, cr, uid, ids, context=None):
        if not context:context={}
        res={}
        for record in self.browse(cr, uid, ids):
            name = "%s - %s"%(record.account_analytic_id.code, record.budget_id.code)
            res.append((record['id'], name))
        return res
        
    _columns ={
              'budget_id':fields.many2one("account.budget.post", "Code", required=True, select=1),
              'budget_code':fields.related("budget_id", "code", type="char", size=8, store=True, select=1),
              'planned_amount':fields.float("Amount", required=True, digits_compute=dp.get_precision('Budget')),
              'account_analytic_id':fields.many2one("account.analytic.account", "Job", ondelete="restrict", select=1),
                }
    _sql_constraints = [
        ('unique_demo_budget_analytic_account', 'unique (budget_id,account_analytic_id)',  'Budget and Job must be unique')]
    _defaults={
               'planned_amount': lambda *x:0.0
               }
    
kderp_demo_budget_data()


class account_budget_post(osv.osv):
    _name = "account.budget.post"
    _inherit = "account.budget.post"
    _description = "Budgetary Position"
    _order = "code, name"
    
    _sql_constraints=[('unique_kderp_demo_budget_code','unique(code)','Code for Budget must be unique !')]
    _columns = {
        'code': fields.char('Code', size=64, required=True),
        'name': fields.char('Name', required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True),
    }
    
    def name_get(self, cr, uid, ids, context=None):
        if not context:
            context={}
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res=[]
        for record in reads:
            name = (record['code']+' - '+record['name']) if record['code'] else record['name']
            res.append((record['id'],name))
        return res
    
account_budget_post()

class account_analytic_account(osv.osv):
    _name='account.analytic.account'
    _inherit='account.analytic.account'

    _columns={
              'kderp_budget_data_line':fields.one2many('kderp.demo.budget.data', 'account_analytic_id', 'Detail of Budget'),
              }
account_analytic_account()
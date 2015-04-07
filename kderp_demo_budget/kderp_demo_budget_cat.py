from openerp.osv import fields, osv
class kderp_demo_budget_category(osv.osv):
    _name = "kderp.demo.budget.category"
    _columns = {

               'name' : fields.char("Name"),
               'cat_code' : fields.char("Code"),
               'parent_id' : fields.many2one('kderp.demo.budget.category','Parent Category', select=True),
               'type' : fields.selection([('expense','Expense'),
                                          ('supervisor','Supervisor'),
                                          ('commission','Commission'),
                                          ('admin','Administration Cost'),
                                          ('profit', 'Profit')
                                          ], 'Type'),
                'budget_post_id':fields.one2many('account.budget.post','budget_categ_id', string='Products'),
                'sequence':fields.integer('Sequence'),
                } 
kderp_demo_budget_category()

class account_budget_account(osv.osv):
    _name = 'account.budget.post'
    _desciption = 'Budgetary Position'
    _inherit = 'account.budget.post'
    
    _columns={
              'budget_categ_id':fields.many2one('kderp.demo.budget.category', 'Category', requires=True, change_default=True),
              }
    def _default_category(self, cr, uid, context={}):
        if context:
            if context.get('budget_categ_id', False):
                return context['budget_categ_id']
        return False
    
    _defaults={
               'budget_categ_id': _default_category,
               }
account_budget_account()
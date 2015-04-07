from openerp.osv import fields, osv
class kderp_demo_budget_category(osv.osv):
    _name = "kderp.demo.budget.category"
    _order = "sequence"
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'],name))
        return res
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context):
        res = self.name_get(cr, uid, ids, context)
        return dict(res)
    
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
                'complete_name':fields.function(_name_get_fnc, string='Name', type='char', metod=True),
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
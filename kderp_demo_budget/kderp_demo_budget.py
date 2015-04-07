from openerp.osv import fields, osv

class kderp_demo_budget(osv.osv):
    _name = "account.budget.post"
    _inherit = "account.budget.post"
    _description = "Budgetary Position"
    
    _order = "code, name"
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
    
kderp_demo_budget()
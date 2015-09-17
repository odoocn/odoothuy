import re
import time

import openerp
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools import float_round, float_is_zero, float_compare
from openerp.tools.translate import _
    
class res_company(osv.osv):
    _inherit = 'res.company'
    _name = 'res.company'
    
    
    _columns={
            'office_ids': fields.one2many('kderp.demo.web.office','company_id', 'Office'),
            'blog_ids': fields.one2many('blog.post','company_id', 'Blog'),
             }
    
    
res_company()

class kderp_demo_web_office(osv.osv):
    _name = 'kderp.demo.web.office'
    _columns = {    
        'company_id': fields.many2one('res.company', 'Company'), 
        'code' : fields.char("Code", translate=True),
        'name' : fields.char("Name", translate=True),
        'address' : fields.char("Address", translate=True),
        'tel' : fields.char("Tel", translate=True),
        'fax' : fields.char("Fax", translate=True)
    }
    
class blog_blog(osv.osv):
    _inherit = 'blog.post'
    _name = 'blog.post'
    _columns={
            'company_id': fields.many2one('res.company', string="Company"),
              }

# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _
# Storing data
class kderp_demo_web_office(osv.Model):
    _name = 'kderp_demo_web.office'
    _columns = {           
        'code' : fields.char("Code", translate=True),
        'name' : fields.char("Name", translate=True),
        'address' : fields.char("Address", translate=True),
        'tel' : fields.char("Tel", translate=True),
        'fax' : fields.char("Fax", translate=True)
    }


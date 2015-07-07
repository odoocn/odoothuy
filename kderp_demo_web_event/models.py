from openerp.osv import fields, osv
import time

class kderp_demo_web_event(osv.osv):
    _name = "kderp.demo.web.event"
    _order = "date desc"
    
    _columns = {
               'code' : fields.char("Code"),
               'name' : fields.char("Name"),
               'date' : fields.date("Date"),
               'description' : fields.text("Description"),
                }
kderp_demo_web_event()

from openerp.osv import fields, osv
class kderp_demo_web_event(osv.osv):
    _name = "kderp.demo.web.event"
    _columns = {
               'code' : fields.char("Code"),
               'name' : fields.char("Name"),
               'date' : fields.date("Date")
                }
kderp_demo_web_event()

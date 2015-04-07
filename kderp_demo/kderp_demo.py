from openerp.osv import fields, osv
class kderp_demo(osv.osv):
    _name = "kderp.demo"
    _columns = {
               'code' : fields.char("Code"),
               'name' : fields.char("Name")
                }
kderp_demo()

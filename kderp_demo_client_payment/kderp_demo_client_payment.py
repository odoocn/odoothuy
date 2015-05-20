from openerp.osv import fields, osv
class kderp_demo_client_payment(osv.osv):
    _name = "kderp.demo.client.payment"
    _columns = {
               'code' : fields.char("Code", required=True),
               'name' : fields.char("Name of Industrial Park", required=True),
               'city' : fields.char("City Province"),
                }
      
kderp_demo_client_payment()

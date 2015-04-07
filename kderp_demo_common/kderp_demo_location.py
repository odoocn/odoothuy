from openerp.osv import fields, osv
class kderp_demo_location(osv.osv):
    _name = "kderp.demo.location"
    _columns = {
               'code' : fields.char("Code", required=True),
               'name' : fields.char("Name of Industrial Park", required=True),
               'city' : fields.char("City Province"),
                }
    
    def name_get(self, cr, uid, ids, context=None):
        reads = self.read(cr, uid, ids, ['name','code'], context=context)
        res = []
        for record in reads:
            name = "%s - %s" % (record['code'],record['name'])
            
            res.append((record['id'], name))
        return res
      
kderp_demo_location()

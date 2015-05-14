from openerp.osv import fields, osv
class ir_attachment(osv.osv):
    _inherit = "ir.attachment"
    _name = "ir.attachment"
    
    def _get_res_id(self, cr, uid, context={}):
        return context.get('res_id', False)
    
    def  _get_res_model(self, cr, uid, context={}):
        return context.get('res_model', False)
    
    def _get_type(self, cr, uid, ctx):
        ctx={}
        return 'binary'
    _columns = {
                #Quotation Attachment
               'q_attached' : fields.boolean("Quotation Attached"),
               'q_attached_be' : fields.boolean("Quotation Budget E Attached"),
               'q_attached_bm' : fields.boolean("Quotation Budget M Attached"),
               'q_attached_qcombine' : fields.boolean("Q.Budget Combine"),
               'q_attached_je' : fields.boolean("Quotation Job Budget E Attached"),
               'q_attached_jm' : fields.boolean("Quotation Job Budget M Attached"),
               'q_attached_jcombine' : fields.boolean("J.Budget Combine"),
               'type' : fields.selection([('url','URL'), ('binary', 'Binary')], 'Type', help="Binary File or URL", required=True),
                }
    
    _defaults={
               'type': _get_type,
               'res_id':_get_res_id,
               'res_model':_get_res_model,
               'q_attached':lambda *a:False,
               'q_attached_be':lambda *a:False,
               'q_attached_bm':lambda *a:False,
               'q_attached_qcombine':lambda *a:False,
               'q_attached_je':lambda *a:False,
               'q_attached_jm':lambda *a:False,
               'q_attached_jcombine':lambda *a:False, 
               }
    def onchange_name(self, cr, uid, ids,name):
        if name:
            val={'value':{'name':name}}
        else:
            val={}
        return val
    
    def onchange_type(self,cr,uid,ids,type):
        if type !='URL' :
            val={'value':{'type':'binary'}}
        else:
            val={'value':{'type':'URL'}}
        return val
ir_attachment()

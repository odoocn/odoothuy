from openerp.osv import fields, osv

class account_analytic_account(osv.osv):
    _name = 'account.analytic.account'
    _inherit = 'account.analytic.account'
    _description = 'Analytic Account'
    
    _rec_name = 'complete_name'
    
    def _get_state(self, cr, uid, ids, name, args, context=None):
        res={}
        for prj in self.browse(cr, uid, ids, context):
            res[prj.id]=prj.state
        return res
    
    def _get_one_full_name(self, elmt, level=6):
        if level<=0:
            return '...'
        if elmt.parent_id and not elmt.type == 'template':
            parent_path = self._get_one_full_name(elmt.parent_id, level-1) + " / "
        else:
            parent_path = ''
        return elmt.code + '-' +elmt.name
     
    def _get_full_name(self, cr, uid, ids, name=None, args=None, context=None):
        if context == None:
            context = {}
        res = {}
        for elmt in self.browse(cr, uid, ids, context=context):
            res[elmt.id] = self._get_one_full_name(elmt)
        return res
    
    def _get_job_to_job_cur(self, cr, uid, ids,context=None):
        result = []
        for kcj in self.pool.get('kderp.demo.project.cur').browse(cr, uid, ids, context=context):
            result.append(kcj.account_analytic_id.id)
        return result
    
    def _get_job_currency(self, cr, uid, ids, name=None, args=None,context=None):
        if context == None:
            context = {}
        res = {}
        var = self.browse(cr, uid, ids, context=context)
        for a in var:
            for b in var.demo_project_cur_ids:
                if b.default_curr:
                    res[a.id]=b.name.id
        return res
    
    def _get_quotation_lists(self, cr, uid, ids, name, arg, context=None):
        res = {}
        job_ids=",".join(map(str,ids))
        
        cr.execute("""SELECT 
                        aaa.id,
                        trim(array_to_string(array_agg(so.id::text),' '))
                    FROM 
                        account_analytic_account aaa
                    left join
                        sale_order so on aaa.id=job_e_id or aaa.id=job_m_id
                    where aaa.id in (%s)
                    group by
                        aaa.id""" % (job_ids))
        for job_id,list_id in cr.fetchall():
            tmp_list=list_id
            if not tmp_list:
                tmp_list=[]
            elif tmp_list.isdigit():
                tmp_list=[int(tmp_list)]
            else:
                tmp_list=list(eval(tmp_list.strip().replace(' ',',').replace(' ','')))
            res[job_id]=tmp_list
        return res
    
    def _get_contract_lists(self, cr, uid, ids, name, arg, context=None):
        res = {}
        job_ids=",".join(map(str,ids))
        
        cr.execute("""SELECT 
                        aaa.id,
                        trim(array_to_string(array_agg(so.contract_id::text),' '))
                    FROM 
                        account_analytic_account aaa
                    left join
                        sale_order so on aaa.id=job_e_id or aaa.id=job_m_id
                    where aaa.id in (%s)
                    group by
                        aaa.id""" % (job_ids))
        for job_id,list_id in cr.fetchall():
            tmp_list=list_id
            if not tmp_list:
                tmp_list=[]
            elif tmp_list.isdigit():
                tmp_list=[int(tmp_list)]
            else:
                tmp_list=list(eval(tmp_list.strip().replace(' ',',').replace(' ','')))
            res[job_id]=tmp_list
        return res
    
    _columns = {
                'code': fields.char('Job No.',size=32, select=True,required=True),
                'name': fields.char('Job Name', size=256, required=True,select=1),
                'complete_name': fields.function(_get_full_name, type='char', string='Full Name'),
                'description':fields.char('Description'),
                'partner_id': fields.many2one('res.partner', 'Client'),    
                'location_id':fields.many2one('kderp.demo.location','Location'),
                #status                                
                'job_type':fields.selection([('E','Electrical'),('M','Mechanical')],"Job Type",select=1),
                'state': fields.selection([('doing','On-Going'),
                                           ('done','Completed'),
                                           ('closed','Closed'),
                                           ('closed_temp','Closed (Temp.)'),
                                           ('cancel','Cancelled')],
                                           "Prj. Status",required=True,select=1, track_visibility='onchange'),
                'process_status':fields.selection([('doing','On-Going'),
                                                   ('done','Completed'),
                                                   ('closed','Closed'),
                                                   ('cancel','Cancelled')],
                                                  "Process Status",select=1),
                
                'state_bar':fields.function(_get_state,selection=[('doing','On-Going'),
                                                                  ('done','Completed'),
                                                                  ('closed','Closed'),
                                                                  ('closed_temp','Closed (Temp.)'),
                                                                  ('cancel','Cancelled')],
                                            type='selection',method=True,string='State Bar',
                                            store={
                                                   'account.analytic.account':(lambda self, cr, uid, ids, c={}: ids, ['state'], 50),
                                                }),
                #date
                'registration_date':fields.date('Reg. Date'),
                'date_start': fields.date('Start Date'),
                'date': fields.date('Closed Date', select=True),
                'completion_date':fields.date('Comp. Date'),
                'actual_completion_date':fields.date('Actual Comp. Date'),
                #user
                'general_project_manager_id':fields.many2one("res.users",'G.P.M.',select=1),
                'user_id': fields.many2one('res.users', 'Project Manager',select=1),
                'manager_id': fields.many2one('res.users', 'Site Manager',select=1),               
                'project_manager_ref':fields.many2one("res.users",'P.M.Ref.',select=1),
                'area_site_manager_id':fields.many2one("res.users",'A.S.M.',select=1),
                'remark':fields.char("Remark"),
                'demo_project_cur_ids':fields.one2many('kderp.demo.project.cur','account_analytic_id','Job Currency'),
                'job_currency':fields.function(_get_job_currency,string='Cur.',type='many2one',method=True,relation='res.currency',
                                               store={
                                                      'kderp.demo.project.cur':(_get_job_to_job_cur, None, 10),
                                                    }),
                #quotation and contract
                'quotation_lists':fields.function(_get_quotation_lists, relation='sale.order',type='one2many',string='Quotations List',method=True),
                'contract_lists':fields.function(_get_contract_lists, relation='demo.contract',type='one2many',string='Contract List',method=True),
                }
                
    

    _defaults={
               'code':lambda *x:'',
               'state':lambda *x:'doing',
               'user_id':lambda *x:'',
               }
    _sql_constraints = [
            ('job_code_unique_code_analytic_account', 'unique (code)',  'Job code must be unique')]
account_analytic_account()
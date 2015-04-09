# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv

class kderp_demo_project_cur(osv.osv):
    _name = 'kderp.demo.project.cur'
    _description = 'Job Currency'
    _order = 'default_curr desc'
    
    def create_currency(self, cr, uid, job_id, context={}):
        if not context: context={}
        curr_obj=self.pool.get('res.currency')
        currency_ids = curr_obj.search(cr, uid, [('id','>',0)])
        new_id = False
        new_ids=[]
        for curr in curr_obj.browse(cr, uid, currency_ids):
            if curr.name == 'USD':
                new_id = self.create(cr, uid, {'name':curr.id,'rate':curr.rate,'account_analytic_id':job_id,'default_curr':False,'rounding':curr.rounding})
                new_ids.append(new_id)
            elif curr.name == 'VND':
                new_id = self.create(cr, uid, {'name':curr.id,'rate':curr.rate,'account_analytic_id':job_id,'default_curr':True,'rounding':curr.rounding})
                new_ids.append(new_id)
        return new_ids
    
    _columns = {
                'name': fields.many2one('res.currency','Curr. Name'),
                'rate':fields.float('Ex.Rate',digits = (12,2),required = True),
                'default_curr':fields.boolean('Default'),
                'rounding':fields.float('Rounding',digits = (12,6)),
                'account_analytic_id':fields.many2one('account.analytic.account','Job'),
                }
kderp_demo_project_cur()
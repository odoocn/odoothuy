from openerp.osv import fields, osv

class kderp_demo_progress_evaluation(osv.osv):
    _name="kderp.demo.progress.evaluation"
    '''
    Module tien do cong viec trong contract 
    '''
    
    _columns={
              'contract_id':fields.many2one('demo.contract','Contract', required=True),
              'name':fields.integer('No.', required=True),
              'currency_id':fields.many2one('res.currency', 'Cur.', required=True),
              'date':fields.date('Date'),
              'advanced':fields.float('Advanced'),
              'retention':fields.float('Retention'),
              'amount':fields.float('Amount'),
              'vat':fields.float('VAT')
              }
    _sql_constraints=[
                      ('progress_evaluation_unique_no', 'unique(contract_id, name, currency_id)', 'Number of Progress and Currency must be unique !')
                      ]
    _defaults={
               'name':1
               }
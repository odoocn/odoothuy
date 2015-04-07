from openerp.osv import fields, osv

class Country(osv.osv):
    _name = 'res.country'
    _description = 'Country'
    _order='name'
    
    _columns = {
        'name': fields.char('Country Name', size=64,
                            help='The full name of the country.', required=True, translate=True),
        'code': fields.char('Country Code', size=2,
                            help='The ISO country code in two chars.\n'
                            'You can use this field for quick search.', required=True),
        'des':fields.text('Description')
    }
    _sql_constraints = [('name_uniq', 'unique (name)', 'The name of the country must be unique !'),
                        ('code_uniq', 'unique (code)', 'The code of the country must be unique !') 
                        ]
    
    def create(self, cursor, user, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(Country, self).create(cursor, user, vals, context=context)
    
    def write(self, cursor, user, ids, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(Country, self).write(cursor, user, ids, vals, context=context)

Country()
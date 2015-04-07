# -*- coding: utf-8 -*-
{
    'name':'Odoo Product',
    'summary': 'First module written by DNT on Odoo with Web',
    'description':'Inherit Product, Customize and Publish to Web site, try using with Group and Permission',
    
    'author': "DNT KDVN-IT-Team",
    'website': "http://www.kinden.co.jp",
     
    'category': 'Learning',
    'version': '1.0',
    'depends':['website','product'],
    'data':[
            'security/odoo_product_security.xml',
            'security/ir.model.access.csv',
            'views/odoo_product.xml',
            'views/templates.xml'
            ],
    'demo':[],
    'tests':[]
}
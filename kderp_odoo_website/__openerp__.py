# -*- coding: utf-8 -*-
{
    'name': "Kderp Odoo Website",
    'summary': """Kderp Odoo Website""",
    'description': """
            This is module Kderp Odoo Website
            """,
    'author': "Team IT Kinden",
    'website': "http://www.kinden.com.vn",
    'category': 'Kderp Odoo Website',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['website','website_partner', 'website_blog','knowledge',],
    # always loaded
    'data': [ 
             'views/blog_post_views.xml',
             'templates.xml'
    ],
    'demo':[
           ]
}
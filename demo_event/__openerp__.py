# -*- coding: utf-8 -*-
{
    'name': "Demo Events",
    'summary': """Demo Events Web""",
    'description': """
            Day la trang web Events ke thua Events odoo
            """,
    'author': "Team IT Kinden",
    'website': "http://www.kinden.com.vn",
    'category': 'Demo Events',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['website_event'],
    # always loaded
    'data': [ 
             'templates.xml',
    ],
    'demo':[
           ]
}
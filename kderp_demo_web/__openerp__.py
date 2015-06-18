# -*- coding: utf-8 -*-
{
    'name': "Kderp Demo Web",
    'summary': """Kderp Demo Web""",
    'description': """
            This is module demo web
            """,
    'author': "Team IT Kinden",
    'website': "http://www.kinden.com.vn",
    'category': 'Kderp Demo Web',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'board','website'],
    # always loaded
    'data': [
            'security/ir.model.access.csv',
            'templates.xml',   
            'views.xml' 
    ],
    'demo':[
           'demo.xml'
           ]
}
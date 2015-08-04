# -*- coding: utf-8 -*-
{
    'name': "Kderp Demo Web Office",
    'summary': """Kderp Demo Web Office""",
    'description': """
            This is module demo web Office
            """,
    'author': "Team IT Kinden",
    'website': "http://www.kinden.com.vn",
    'category': 'Kderp Demo Web Office',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'board','website'],
    # always loaded
    'data': [ 
             #'security/ir.model.access.csv',
             'views.xml',
             #'templates.xml',
    ],
    'demo':[
           ]
}
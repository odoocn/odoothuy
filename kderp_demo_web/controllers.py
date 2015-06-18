# -*- coding: utf-8 -*-
from openerp import http
# To the browser
# class Academy(http.Controller):
#     @http.route('/academy/academy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"
  
#Template  
# class Academy(http.Controller):
#     @http.route('/academy/academy/', auth='public')
#     def index(self, **kw):
#         return http.request.render('kderp_demo_web.index', {
#             'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],})

#Lay du lieu tu demo
#Accessing the data
# class Academy(http.Controller):
#     @http.route('/academy/academy/',auth='public')
#     def index(self, **kw):
#         #goi cac du lieu mau
#         Teachers = http.request.env['kderp_demo_web.teachers']
#         return http.request.render('kderp_demo_web.index',{
#             'teachers':Teachers.search([])
#             })

#Website support
class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['kderp_demo_web.teachers']
        return http.request.render('kderp_demo_web.index',{
            'teachers':Teachers.search([])                                              
            })

#URLs and routing
    @http.route('/academy/<name>/', auth='public', website=True)
    def teacher(self, name):
        return '<h1>{}</h1>'.format(name)
    
    @http.route('/academy/academy/', auth="public", website=True)
    def teacher(self, id):
        return '<h1>{}</h1>'.format(id, type(id).__name__)
    
    @http.route('/academy/<model("kderp_demo_web.teachers"):teacher>', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('kderp_demo_web.biography',{
            'person': teacher                                                    
             })
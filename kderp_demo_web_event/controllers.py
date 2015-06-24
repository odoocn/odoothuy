from openerp import http

class kderp_demo_web_event(http.Controller):
    @http.route('/demo/event/', auth='public', website=True)
    def index(self, **kw):
        names_var = http.request.env['kderp.demo.web.event']
        return http.request.render('kderp_demo_web_event.index',{
            'name_a' : names_var.search([])
                                                                 })

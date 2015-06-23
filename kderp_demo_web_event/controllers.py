from openerp import http

class kderp_demo_web_event(http.Controller):
    @http.route('/demo/event/', auth='public')
    def index(self, **kw):
        return "Hello Word!"
# -*- coding: utf-8 -*-
import openerp.addons.web.http as http

class SimpleController(http.Controller):
    _cp_path = '/event'
    #/event tuong tu nhu /event/index
    @http.httprequest
    def index(self, req, s_action=None, **kw):

        SIMPLE_TEMPLATE = """
                            <html>
                                <head>
                                    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
                                    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
                                    <title>OpenERP V7 Simple Web Controller Example using HttpRequest</title>
                                </head>
                                <body>
                                    <form action="/event/Page2" method="POST">
                                        <button name="GoToPage2" value="*">Go To Page 2</button>
                                    </form>
                                </body>
                            </html>
                            """
        return SIMPLE_TEMPLATE

    @http.httprequest
    def Page2(self, req, s_action=None, **kw):
        Page2_View = "<html><head></head><body>AND NOW YOU'RE ON PAGE 2</body></html>"
        return Page2_View
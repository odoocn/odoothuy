from openerp import http
from openerp.http import request

try:
    from openerp.addons.website_booking_calendar.controllers.main import website_booking_calendar as controller
except ImportError:
    class controller(object):
        pass

class website_booking_calendar(controller):

    def _get_template(self, params):
        if params.get('backend', False):
            return 'website_booking_calendar.iframe'
        else:
            return super(website_booking_calendar, self)._get_template(params)

    @http.route(['/booking/calendar/validate'], type='json', auth='public', website=True)
    def validate(self, start, end, calendar_id):
        pass
        


        


import functools
import xmlrpclib

HOST = '192.168.0.91'
PORT = 8009
DB = 'Odoo'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%s/xmlrpc/' % (HOST, PORT)

# TODO: 1. login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print "Logged in as %s (uid:%s)" % (USER, uid)
call = functools.partial(
        xmlrpclib.ServerProxy(ROOT + 'object').execute, DB, uid, PASS)

# TODO: 2. Read the Session
Object = 'openacademy.session'
sessions = call(Object, 'search_read', [], ['name', 'seats'])
for session in sessions:
    print "Session %s (%s seats)" % (session['name'], session['seats'])
    
# TODO: 3. Create a new Session
course_id = call('openacademy.course', 'search', [('name','ilike','Python')])
if course_id:
    sessions = call(Object, 'create', {
                                                'name': 'New Sessions from Web service',
                                                'course_id': course_id[0]})
    
# TODO: 4 Create tesintg task
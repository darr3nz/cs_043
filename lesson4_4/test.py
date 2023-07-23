import wsgiref.simple_server
import urllib.parse
from lesson4_projects.httpdb import Simpledb

db = Simpledb('htmldb.txt')

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    print(path)
    print(params)

    if path == '/select':
        start_response('200 OK', headers)
        find_name = params['key'][0]

        if find_name:

            db.find(find_name)
            return [phone.encode()]
        else:
            return ['NULL'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()

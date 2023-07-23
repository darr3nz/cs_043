import wsgiref.simple_server
import urllib.parse
from httpdb import Simpledb

db = Simpledb('httpdb.txt')

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])

    if len(path) == 1:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]

    if path == '/insert':
        if len(params) != 2 or list(params.keys())[0] != 'key' or list(params.keys())[1] != 'value':
            start_response('404 Not Found', headers)
            return ['Status 404: parameter not found'.encode()]
        else:
            start_response('200 OK', headers)
            name = params['key'][0]
            phone_number = params['value'][0]
            db.add(name, phone_number)
            return ['Inserted'.encode()]
    elif path == '/select':
        if len(params) != 1 or list(params.keys())[0] != 'key':
            start_response('404 Not Found', headers)
            return ['Status 404: parameter not found'.encode()]
        else:
            start_response('200 OK', headers)
            find_name = params['key'][0]
            found_phone = db.find(find_name)
            if found_phone != '':
                return [found_phone.encode()]
            else:
                return ['Not found'.encode()]
    elif path == '/delete':
        if len(params) != 1 or list(params.keys())[0] != 'key':
            start_response('404 Not Found', headers)
            return ['Status 404: parameter not found'.encode()]
        else:
            start_response('200 OK', headers)
            delete_name = params['key'][0]
            found = db.delete(delete_name)
            if found:
                return ['Deleted'.encode()]
            else:
                return ['Not found'.encode()]
    elif path == '/update':
        if len(params) != 2 or list(params.keys())[0] != 'key' or list(params.keys())[1] != 'value':
            start_response('404 Not Found', headers)
            return ['Status 404: parameter not found'.encode()]
        else:
            start_response('200 OK', headers)
            update_name = params['key'][0]
            update_phone_number = params['value'][0]
            found = db.update(update_name, update_phone_number)
            if found:
                return ['Updated'.encode()]
            else:
                return['Not found'.encode()]
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()

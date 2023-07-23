import wsgiref.simple_server
# URL http://localhost:8001

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response('200 OK', headers)
    return ['Good morning, Sunshine!'.encode()]

httpd = wsgiref.simple_server.make_server('', 8001, application)
httpd.serve_forever()

import wsgiref.simple_server
import http.cookies


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8'),
               ('Set-Cookie', 'favoriteColor=red'),
               ('Set-Cookie', 'favoriteNumber=4'),
               ('Set-Cookie', 'name=Jason')
    # Set cookies here . . .

]
    start_response('200 OK', headers)

    # Cookie parser goes here . . .
    cookies = http.cookies.SimpleCookie()
    cookies.load('favoriteColor=red; favoriteNumber=4; name=Jason')

    cookie = ""
    for key in cookies:
        print(key + '=' + cookies[key].value)
        cookie = cookie + (key + '=' + cookies[key].value)

    return [cookie.encode()]
httpd = wsgiref.simple_server.make_server('', 8000, application)

print("Serving on port 8000...")

httpd.serve_forever()

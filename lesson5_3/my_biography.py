import wsgiref.simple_server

def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response('200 OK', headers)

    path = environ['PATH_INFO']
    if path == '/biography':
        page = '''<!DOCTYPE html>
        <html><head><title>Biography</title></head><body>
        <h1>Hi, I'm Darren Zhuang</h1>
        <h2 style="background-color: aqua"> I like video games</h2>
        <p> Minecraft is cool</p>
        <p style="color: blue"> Here are some other things I like</p>
        <p> Things I like </p>
        <p>Money <a href="https://upload.wikimedia.org/wikipedia/commons/2/23/US_one_dollar_bill%2C_obverse%2C_series_2009.jpg">Big Bucks</a></p>
        <p> Spongebob <a href="https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/1200px-SpongeBob_SquarePants_character.svg.png"> Spongebob</a></p>
        <br />
        <img style="border:5px solid" src="https://cdn.icon-icons.com/icons2/2699/PNG/512/minecraft_logo_icon_168974.png" />
        <p>By David Bachrach (1845-1921) [Public domain], via Wikimedia Commons</p>
        </body>
        </html>'''
    else:
        return ['404 Not Found'.encode()]
    return [page.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()

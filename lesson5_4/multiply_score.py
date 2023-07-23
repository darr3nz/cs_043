import wsgiref.simple_server
import urllib.parse
import http.cookies
import random
import sqlite3

connection = sqlite3.connect('users.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()

# If someone does not have the table in the database, the code does so
if (r == []):
    exp = 'CREATE TABLE users (username,password)'
    connection.execute(exp)
    connection.commit()

def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None
    factor1 = params['factor1'][0] if 'factor1' in params else None
    factor2 = params['factor2'][0] if 'factor2' in params else None
    answer = params['answer'][0] if 'answer' in params else None

# If the user puts /register in the path with a username and password, the users account will be registered
    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            headers.append(('Set-Cookie', 'session={}:{}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(un, pw)))
            connection.execute('INSERT INTO users VALUES(?, ?)', [un, pw])
            connection.commit()
            return ['Successfully registered your account. Click here to go to your account and start the game <a href="http://localhost:8000/account?username={}&password={}"> here </a>'.format(un, pw).encode()]
# If the user puts /register without a username and password, they will be sent to a page that will make them put a username and password to create an account
    elif path == '/register':
        start_response('200 OK', headers)
        headers.append(('Set-Cookie', 'session={}:{}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(un, pw)))
        register_page = '''<!DOCTYPE HTML>
        <h2> Register </h2>
        <p> Enter in an username and password </p>
        <form>
        Username <input type="text" name="username"><br>
        Password <input type="password" name="password"><br>
        <input type="submit">
        </form>
        '''
        return [register_page.encode()]
# If the user puts /login in the path with a username and password, the program will log them in to their account
    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. Go to your account to play. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password. <a href="/">Please login again.</a>'.encode()]
# If the user puts /logout in the path, they will log out of their account
    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]
# If the user puts /account, the game would start
    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()

        #This is where the game begins. This section of is code only executed if the login form works, and if the user is successfully logged in
        if user:
            cookies = http.cookies.SimpleCookie()
            if 'HTTP_COOKIE' in environ:
                cookies.load(environ['HTTP_COOKIE'])

            if 'correct' in cookies:
                correct = int(cookies['correct'].value)
            else:
                correct = 0
            if 'wrong' in cookies:
                wrong = int(cookies['wrong'].value)
            else:
                wrong = 0

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'
            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                true_answer = int(factor1) * int(factor2)
                if int(answer) == true_answer:
                    page = page + '<h1 style="background-color: lightgreen"> Correct, {} x {} = {} </h1>'.format(factor1, factor2, answer)
                    correct = int(cookies['correct'].value) + 1
                    wrong = int(cookies['wrong'].value)
                else:
                    page = page + '<h1 style="background-color: red"> Wrong, {} x {} = {} </h1>'.format(factor1, factor2, true_answer)
                    wrong = int(cookies['wrong'].value) + 1
                    correct = int(cookies['correct'].value)

            headers.append(('Set-Cookie', 'correct={}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(correct)))
            headers.append(('Set-Cookie', 'wrong={}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(wrong)))
            headers.append(('Set-Cookie', 'score={}:{}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(correct, wrong)))

            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1
            correct_answer = f1 * f2
            answer_list = [correct_answer, correct_answer+random.randrange(1,20), correct_answer-random.randrange(1,20), correct_answer+random.randrange(21,40)]
            page = page + '<h1>What is {} x {}?</h1>'.format(f1, f2)
            random.shuffle(answer_list)
            label_list = ['A', 'B', 'C', 'D']
            for i in range(4):
                ans = f1 * f2
                page = page + '{}: <a href="http://localhost:8000/account?factor1={}&amp;factor2={}&amp;answer={}">{}</a> <br>'.format(label_list[i], f1, f2, answer_list[i], answer_list[i])

            if 'reset' in params:
                correct = 0
                wrong = 0
                headers.append(('Set-Cookie', 'correct={}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(correct)))
                headers.append(('Set-Cookie', 'wrong={}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(wrong)))
                headers.append(('Set-Cookie', 'score={}:{}; expires=Wed, 25 Dec 2030 00:01:00 GMT'.format(correct, wrong)))

            page += '''<h2>Score</h2>
            <b>Correct: {}</b><br>
            <b>Wrong: {}</b><br><br>
            <form action="/account">
            <a href="/account?reset=true">Reset Score</a>
            </form>
            <br>
            <a href="/logout">Logout</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]
# This elif path below creates two forms that will let the user log in to an account or register one
    elif path == '/':
        start_response('200 OK', headers)
        path_none_page = '''<!DOCTYPE html>
        <h2>You need to log in to play the game.</h2>
        <p>Please login:</p>
        <form  action="/login">
        Username <input type="text" name="username"><br>
        Password <input type="password" name="password"><br>
        <input type="submit">
        </form>
        <br><br>
        <form>
        <p>If you do not have an account, please <a href="/register">register</a>.</p>
        </form>
        '''
        return [path_none_page.format(un, pw).encode()]
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()

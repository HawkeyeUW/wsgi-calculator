"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
def main():
    body = ['<h1>WSGI Calculator</h1>', '<ul>']
    body.append('<h3>This calculator will do simple  +,  -,  * and  / with two numbers.</h3>')
    body.append('<ul>')
    body.append('<html>Instructions......</html>')
    body.append('<li>First parameter will be add, subtract, multiply or divide</li>')
    body.append('<li>Second parameter of path will be the first number</li>')
    body.append('<li>Third parameter of the path will be the second number</li>')
    body.append('<li>Example: /add/5/2 will yield 7</li>')

    return '\n'.join(body)

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    digit1 = args[0]
    digit1 = int(digit1)

    digit2 = args[1]
    digit2 = int(digit2)

    sum = digit1 + digit2

    page = ['<h1>Addition Calculator Results</h1>']
    page.append(f'<html> {digit1} + {digit2} = {sum}<html>')
    return '\n'.join(page)

def subtract(*args):
    digit1 = args[0]
    digit1 = int(digit1)

    digit2 = args[1]
    digit2 = int(digit2)

    subtract = digit1 - digit2

    page = ['<h1>Subtraction Calculator Results</h1>']
    page.append(f'<html> {digit1} - {digit2} = {subtract}<html>')
    return '\n'.join(page)

def multiply(*args):
    digit1 = args[0]
    digit1 = int(digit1)

    digit2 = args[1]
    digit2 = int(digit2)

    multiply = digit1 * digit2

    page = ['<h1>Multiplication Calculator Results</h1>']
    page.append(f'<html> {digit1} * {digit2} = {multiply}<html>')
    return '\n'.join(page)

def divide(*args):
    digit1 = args[0]
    digit1 = int(digit1)

    digit2 = args[1]
    digit2 = int(digit2)

    divide = digit1 / digit2

    page = ['<h1>Division Calculator Results</h1>']
    page.append(f'<html> {digit1} / {digit2} = {divide}<html>')
    return '\n'.join(page)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': main,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    content_path = environ['url']
    if content_path == "/index.py":
        return "index.py is show"
    elif content_path == "/center.py":
        return "center.py is show"
    elif content_path == "/login.py":
        return "我登录!"
    else:
        return "not page is find!"
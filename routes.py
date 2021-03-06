from utils import log
from models import User
from models import Message
import random


messages = []


def route_index(request):
    headers = "HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n"
    body = '<h1>Hello World</h1><img src="doge.gif"/>'
    r = headers + "\r\n" + body
    return r.encode(encoding='utf-8')


def route_image(request):
    with open('./templates/doge.gif', 'rb') as f:
        headers = b'HTTP/1.1 200 ok\r\nContent-Type: img/gif\r\n\r\n'
        return headers + f.read()


def template(filename):
    # 打开模板函数
    path = './templates/' + filename
    with open(path, encoding='utf-8') as f:
        return f.read()


def error(status_code=404):
    error_info = {
        404: b'HTTP/1.1 404 Not Found\r\n\r\n<h1>Not Found</h1>'
    }

    return error_info.get(status_code, b'')


def route_login(request):

    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': '',
    }
    log.log('request.cookies: ', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            session_id = random_str()
            session[session_id] = u.username
            headers['Set-Cookie'] = 'username={}'.format(session_id)
            result = "登录成功"
        else:
            result = "用户名或密码错误"
    else:
        result = ''
    body = template('login.html')

    body = body.replace('{{username}}', username)

    body = body.replace('{{result}}', result)
    response = respone_with_headers(headers, 200) + body
    log.log("response", response)
    return response.encode('utf-8')


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = './static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.0 200 ok\r\nContent-Type: img/gif\r\n\r\n'
        body = f.read()
        # 返回响应头和响应体
        return header + body


def redirect(url):
    """
    浏览器收到状态码302的时候，会在headers里面查找一个'Location'的字段并获取一个url，然后自动请求新的url
    :param url:
    :return:
    """
    headers = {
        'Location': url,
    }

    response = respone_with_headers(headers, 302)
    log.log("redirect ", response)
    return response.encode('utf-8')


def route_message(request):

    username = current_user(request)
    if username == '【游客】':
        url = '/'
        return redirect(url)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        messages.append(msg)
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in messages])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    注册功能
    :return:
    """
    log.log("router_register: ", request.method)
    header = 'HTTP/1.0 200 ok\r\nContent-Type: text/html\r\n\r\n'
    if request.method == 'POST':
        form = request.form()
        user = User(form)
        log.log('route_register: ', user)
        if user.validate_register():
            user.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2.'
    else:
        result = '123'
    body = template('register.html')
    # log.log("router_register: ", body)
    body = body.replace('{{result}}', result)
    # body = body.replace('{{username}}', u.username)
    # log.log("body + header", header)
    response = header + body
    return response.encode('utf-8')


def response_for_path(req):
    path = req.path
    log.log("routes, path", path)
    respone_function = route_dict.get(path, error)
    # log.log("routes, reponse", respone_function(req))

    # 在返回值的时候调用函数
    return respone_function(req)


def respone_with_headers(headers, status_code):
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    header = header + '\r\n'
    return header


def current_user(request):
    session_id = request.cookies.get('username')
    username = session.get(session_id, '【游客】')
    return username


def random_str():
    seed = 'qwertyuiopasdfghjklzxcvbnm'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


route_dict = {
    '/': route_index,
    '/doge.gif': route_image,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}

session = {}


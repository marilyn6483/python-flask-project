def route_index():
    headers = "HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n"
    body = '<h1>Hello World</h1><img src="doge.gif"/>'
    r = headers + "\r\n" + body
    return r.encode(encoding='utf-8')


def route_image():
    with open('./templates/doge.gif', 'rb') as f:
        headers = b'HTTP/1.1 200 ok\r\nContent-Type: img/gif\r\n\r\n'
        return headers + f.read()


def page_html():
    with open('./templates/html_basic.html', 'rb') as f:
        headers = b'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n\r\n'
        return headers + f.read()


def error(status_code=404):
    error_info = {
        404: b'HTTP/1.1 404 Not Found\r\n\r\n<h1>Not Found</h1>'
    }

    return error_info.get(status_code, b'')


def login():
    with open('./templates/login.html', 'rb') as f:
        headers = b'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n\r\n'
        return headers + f.read()


def response_for_path(path):
    url_router = {
        '/': route_index,
        '/doge.gif': route_image,
        '/page': page_html,
        '/login': login,
    }
    respone_function = url_router.get(path, error)

    # 在返回值的时候调用函数
    return respone_function()
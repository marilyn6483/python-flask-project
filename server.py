import socket


def log(*args, **kwargs):
    print("log: ", *args, **kwargs)


def route_index():
    headers = "HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n"
    body = '<h1>Hello World</h1><img src="doge.gif"/>'
    r = headers + "\r\n" + body
    return r.encode(encoding='utf-8')


def route_image():
    with open('./templates/doge.gif', 'rb') as f:
        return f.read()
    # pass


def error(status_code=404):
    error_info = {
        404: b'HTTP/1.1 404 Not Found\r\n\r\n<h1>Not Found</h1>'
    }

    return error_info.get(status_code, b'')

def response_for_path(path):
    url_router = {
        '/' : route_index(),
        '/doge.gif': route_image(),
    }

    return url_router.get(path, error())


def run(host='127.0.0.1', port=2000):

    with socket.socket() as s:
        # 绑定到指定的port
        s.bind((host, port))

        # 使用无线循处理请求
        while True:
            # server在监听
            s.listen(5)
            # 获取到一个连接和客户端ip
            connection, address = s.accept()
            # connection用于接受客户端发来的请求,发送服务端的响应，并关闭连接，返回的request是一个bytes

            # 取出完整的数据
            r = b''
            buffer_size = 1000
            while True:
                req = connection.recv(buffer_size)
                r += req
                if len(r) < buffer_size:
                    break

            log('ip and port: ', address)
            log('request: ', r.decode('utf-8'))

            request = r.decode('utf-8')

            try:
                path = request.split(" ")[1]
                log('path: ', path)
                response = response_for_path(path)

                connection.sendall(response)
            except Exception as e:
                log('error: ', e)

            connection.close()


if __name__ == '__main__':
    run()

import socket
from utils import log
from routes import *
import urllib.parse


class Request:
    def __init__(self):
        self.path = '/'
        self.method = 'GET'
        self.query = {}
        self.body = ''

    def form(self):
        """
        解析body，返回表单提价参数参数字典
        :return:
        """
        # body = urllib.parse.unquote(self.body)
        # log.log("self.body: ", body)
        params = self.body.split('&')
        args = {}
        for param in params:
            log.log('param: ', param)
            k, v = param.split('=')
            # 解码空格unquote_plus
            v = urllib.parse.unquote_plus(v, encoding='utf-8')
            args[k] = v

        return args

    def parse_request(self, request):
        header = request.split("\r\n\r\n")[0]
        self.body = request.split("\r\n\r\n")[1]
        headers = header.split("\r\n")
        self.method = headers[0].split(' ')[0]
        self.path = headers[0].split(' ')[1]


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
                if len(req.decode('utf-8').split()) < 2:
                    continue
                r += req
                if len(r) < buffer_size:
                    break

            log.log('ip and port: ', address)
            log.log('request: ', r.decode('utf-8'))

            request = r.decode('utf-8')
            req = Request()
            req.parse_request(request)
            path = req.path
            if req.body:
                args = req.form()
                log.log("self.args: ", args)
            log.log("self.path: ", path)

            try:
                # path = request.split(" ")[1]
                response = response_for_path(req)
                log.log('response: ', response)
                connection.sendall(response)
            except Exception as e:
                log.log('error: ', e)

            connection.close()


if __name__ == '__main__':
    run()

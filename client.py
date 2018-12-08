import socket
import ssl


def parsed_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    '''
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split("://")[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split("://")[1]
    else:
        u = url
    index = u.find('/')
    print(u.split('/'))
    if index == -1:
        host = u
        path = '/'
    else:
        host = u.split('/')[0]
        path = u.split('/')[1]
        print(host, path)

    port_dict = {
        'http': 80,
        'https': 443,
    }
    port = port_dict[protocol]

    if ':' in host:
        index = host.find(":")
        host = host[:index]
        port = int(host[index:])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    s = socket.socket()
    if protocol == 'http':
        return s
    if protocol == 'https':
        return ssl.wrap_socket(s)


def response_by_socket(s):
        # connection, address = s.accept()
        # s.listen(5)
    buffer_size = 1024
    r = b''
    while 1:
        res = s.recv(buffer_size)
        r += res
        if len(res) < buffer_size:
            break

    return r


def parsed_response(response):
    print(response)
    headers = response.split("\r\n\r\n")[0]
    body = response.split("\r\n\r\n")[1]

    # print(headers)
    eles = headers.split("\r\n")
    status_code = eles[0].split(" ")[1]
    # print(status_code)
    header_dict = {}
    # print(eles)
    for line in eles[1:]:
        k, v = line.split(": ")
        header_dict[k] = v
    return status_code, header_dict, body


def get(url):
    '''
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    '''
    protocol, host, port, path = parsed_url(url)
    # print(parsed_url(url))
    s = socket_by_protocol(protocol)

    s.connect((host, port))
    request = 'GET /{} HTTP/1.1\r\nHost: {}:{}\r\nConnection: close\r\n\r\n'.format(path, host, port)
    print(request)
    s.send(request.encode('utf-8'))
    r = response_by_socket(s)
    response = r.decode('utf-8')
    status_code, headers, body = parsed_response(response)
    if status_code in ['301', '302']:
        url = headers['Location']
        return get(url)
    return status_code, headers, body


def main():
    url = 'http://movie.douban.com/top250'
    # r = get(url)
    # print(r)
    # host = host_of_url(url)
    # print(host)


if __name__ == '__main__':

    print(get('https://movie.douban.com/top250'))


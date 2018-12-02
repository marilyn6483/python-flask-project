import socket

host = ""
port = 80

# AF_INET:实现ipv4协议;SOCK_STREAM:TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 如果要实现https的话，使用ssl
# import ssl
# s = ssl.wrap_socket(s)

# 连接主机
s.connect((host, port))

# 获取本机ip和port
ip, local_port = s.getsockname()

# 构造一个HTTP请求
http_request= "Get /HTTP/1.1\r\n\r\nhost:{}\r\n\r\n".format(ip)
request = http_request.encode("utf-8")
s.send(request)

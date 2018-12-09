import socket

host = "g.cn"
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
print("本机IP和端口：", ip, local_port)

# 构造一个HTTP请求
http_request= "Get /HTTP/1.1\r\n\r\nhost:{}\r\n\r\n".format(ip)

# 转换成bytes之后传输出去
request = http_request.encode("utf-8")
s.send(request)

# 接受数据
response = s.recv(1023)
response = response.decode("utf-8")

# print("response:", response)

# 解析响应
# print(response.split("\r\n\r\n")[0])
# 获取响应headers和body
headers = response.split("\r\n\r\n")[0]
body = response.split("\r\n\r\n")[-1]

# print(headers)
eles = headers.split("\r\n")
status_code = eles[0].split(" ")[1]
print(status_code)
header_dict = {}
print(eles)
for ele in eles[1:]:
    print(ele.split(":")[0])
    header_dict[ele.split(":")[0]] = ele.split(":")[1]
print(header_dict)
# {'Content-Type': ' text/html; charset=UTF-8', 'Referrer-Policy': ' no-referrer', 'Content-Length': ' 1555', 'Date': ' Mon, 03 Dec 2018 10'}



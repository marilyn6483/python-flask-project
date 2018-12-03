import socket


host = "127.0.0.1"
# 1024以下的port是系统保留的端口，以上的数字可以任意选择
port = 2000

s = socket.socket()
# 绑定到指定的port
s.bind((host, port))

# 使用无线循处理请求
while True:
    # server在监听
    s.listen(5)
    # 获取到一个连接和客户端ip
    connection, ip = s.accept()
    # connection用于接受客户端发来的请求，返回的request是一个bytes
    request = connection.recv(1024).decode("utf-8")
    print("ip and request", ip, request)
    response = "HTTP/1.1 200 ok\r\n\r\n <h1>hello</h1>".encode("utf-8")
    connection.sendall(response)
    connection.close()
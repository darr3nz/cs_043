def http_head(host, page):
    import socket
    sock = socket.create_connection((host,80))
    sock.sendall(('Head' + page + ' HTTP/1.1\r\nHost:' + '\r\n\r\n').encode())
    print(sock.recv(1000).decode())
    sock.close()
http_head('www.google.com', '/')

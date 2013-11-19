#encoding=utf-8

if __name__ == '__main__':
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 52070))
    say = raw_input(u'说点什么...\n')
    sock.send(str(say))
    print sock.recv(1024)
    sock.close()

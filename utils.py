import socket


def send(conn: socket.socket, str: str):
    print('sending:', str)
    conn.send(bytes(str + '\0', 'utf8'))


def read(conn):
    bytes = b''
    data = conn.recv(1024)
    while data:
        bytes += data
        if bytes.endswith(b'\0'):
            bytes = bytes.strip(b'\0')
            break
        try:
            data = conn.recv(1024)
        except socket.error:
            if bytes == b'':
                return 'err'
            break
    print('read:', bytes.decode('utf8'))
    return bytes.decode('utf8')
import socket


def send(conn: socket.socket, str: str):
    conn.sendall(bytes(str, 'utf8') + b'\0')


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
    return bytes.decode('utf8')

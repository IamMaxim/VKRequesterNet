import socket
import ssl
import threading
import utils

# list with all active listeners
clients = []


def serve_client(client, addr, req):
    client.settimeout(None)
    # client is ready to receive VK requests
    if req == 'LISTENING':
        print('Adding listener', addr[0])
        clients.append(client)
        utils.send(client, 'You have been added as listener.')
    # client sent VK request that should be run on all listeners
    elif req.startswith('MESSAGE'):
        print('sending to all message "', req, '" from ', addr[0], sep='')
        # todo: add check
        for c in clients:
            try:
                utils.send(c, req)
            except socket.error:
                # socket closed; remove it from listeners
                print('Removing listener', addr[0])
                clients.remove(c)


def start_server(port):
    sock = ssl.wrap_socket(socket.socket(), 'server.key', 'server.crt', True)
    # handle situation when port is already in use
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    # set max users to 1024
    sock.listen(1024)
    print('Server started at port', port)

    while True:
        # accept new connection
        conn, addr = sock.accept()
        # read client request
        req = utils.read(conn)

        # shutdown server
        if req == 'STOP':
            print('Received STOP command from', addr[0])
            break

        # handle client in another thread
        t = threading.Thread(target=serve_client, args=(conn, addr, req))
        t.run()

    print('Shutting down server...')
    # close connection with all listeners
    for c in clients:
        utils.send(c, 'STOP')
        c.close()
    sock.close()


start_server(46821)

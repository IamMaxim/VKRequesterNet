import socket
import ssl
import threading
import utils
import subprocess
import json
import user
import hashlib

# list with all active listeners
clients = []
users = {}
hasher = hashlib.md5()


def loadUsers():
    try:
        file = open('users.db', 'r+')
        while True:
            line = file.readline()
            if line != '':
                u = user.User(obj=json.loads(line))
                users[u.login] = u
            else:
                break
        print('users.db loaded')
    except FileNotFoundError:
        print('users.db not found')


def saveUsers():
    file = open('users.db', 'w+')
    for u in users.values():
        file.write(str(u) + '\n')
    print('users.db saved')


def exec(client: socket.socket, command: str):
    utils.send(client, subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf8'))


def message(client, addr, req):
    print('sending to all message "', req, '" from ', addr[0], sep='')
    # todo: add check
    for c in clients:
        try:
            utils.send(c, req)
        except socket.error:
            # socket closed; remove it from listeners
            print('Removing listener', addr[0])
            clients.remove(c)


def register(client, addr, req):
    utils.send(client, 'Enter login: ')
    login = utils.read(client)
    utils.send(client, 'Enter password: ')
    hasher.update(utils.read(client))
    passhash = hasher.hexdigest()
    print('passhash:', passhash)
    utils.send(client, 'Enter nickname: ')
    nick = utils.read(client)
    u = user.User(login=login, passhash=passhash, nick=nick, permission=0)
    users[u.login] = u
    utils.send(client, 'Registered successfully')
    print('Registered user', u.nick)
    return u


def login(client, addr, req):
    utils.send(client, 'Enter login: ')
    login = utils.read(client)
    utils.send(client, 'Enter password: ')
    hasher.update(utils.read(client))
    passhash = hasher.hexdigest()
    print('passhash:', passhash)
    u = users[login]
    if u:
        if passhash == u.passhash:
            utils.send(client, 'Logged in as ' + u.nickname)
            return u
        else:
            utils.send(client, 'Login failed')
            return 'err'


def serve_client(client, addr):
    print('serving', addr[0] + ':' + str(addr[1]))
    try:
        client.settimeout(None)
        user = 'err'
        req = utils.read(client)
        # client is ready to receive VK requests
        if req == 'LISTENING':
            print('Adding listener', addr[0])
            clients.append(client)
            utils.send(client, 'You have been added as listener.')
        # client sent VK request that should be run on all listeners
        else:
            while True:
                if req == '':
                    return

                if req == 'REGISTER':
                    user = register(client, addr, req)
                if user == 'err':
                    user = login(client, addr, req)
                if user == 'err':
                    utils.send(client, 'STOP')
                    client.close()
                    return

                if req == 'STOP':
                    if user.permission >= 2:
                        print('Received STOP command from', addr[0])
                        global needToRun
                        needToRun = False
                    else:
                        utils.send(client, 'You do not have permission to do that')
                if req.startswith('MESSAGE'):
                    if user.permission >= 1:
                        message(client, addr, req)
                elif req.startswith('EXEC'):
                    if user.permission >= 2:
                        comm = req[4:]
                        print('Executing command "', comm, '" from ', addr[0], sep='')
                        exec(client, comm)
                req = utils.read(client)
    except Exception:
        Exception
        client.close()


needToRun = True
def start_server(port):
    sock = ssl.wrap_socket(socket.socket(), 'server.key', 'server.crt', True)
    # handle situation when port is already in use
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    # set max users to 1024
    sock.listen(1024)
    print('Server started at port', port)

    while needToRun:
        # accept new connection
        conn, addr = sock.accept()

        # handle client in another thread
        threading.Thread(target=serve_client, args=(conn, addr)).start()

    print('Shutting down server...')
    # close connection with all listeners
    for c in clients:
        utils.send(c, 'Server is shutting down...')
        utils.send(c, 'STOP')
        c.close()
    sock.close()


loadUsers()
start_server(5003)
saveUsers()

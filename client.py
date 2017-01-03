import socket
import ssl
import utils
import vkapi
import json

vk = vkapi.vkapi(open('access_token.txt').read())


def processMessage(msg):
    obj = json.loads(msg)
    print('response:', vk.sendRequest(obj['name'], obj['useToken'], obj['args']))


def startListening():
    while True:
        # read request or plain text
        res = utils.read(sock)
        print(res)
        if res == '' or res == 'err' or res == 'STOP':
            break
        if res.startswith('MESSAGE'):
            # remove MESSAGE and process
            processMessage(res[7:])


sock = ssl.wrap_socket(socket.socket())
sock.connect(('localhost', 46821))

# utils.send(sock, 'STOP')
# utils.send(sock, 'MESSAGE and some more text')
# utils.send(sock, 'LISTENING')
# startListening()
utils.send(sock, 'MESSAGE' + json.dumps({'name': 'users.get', 'useToken': False, 'args': ['user_id=1', 'fields=first_name,last_name']}))

print('Shutting down...')
sock.close()

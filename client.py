import socket
import ssl
import utils
import vkapi
import json
import threading

vk = vkapi.vkapi(open('access_token.txt').read().strip('\n'))


def processMessage(msg):
    obj = json.loads(msg)
    print('response:', vk.sendRequest(obj['name'], obj['useToken'], obj['args']))


def startListening():
    print('starting listening...')
    while True:
        # read request or plain text
        res = utils.read(sock)
        print(res)
        if res == '' or res == 'err' or res == 'STOP':
            print('Server closed connection')
            break
        if res.startswith('MESSAGE'):
            # remove MESSAGE and process
            processMessage(res[7:])


sock = ssl.wrap_socket(socket.socket())
sock.connect(('localhost', 5003))

listener = threading.Thread(target=startListening)
listener.start()
print('listener thread started.')
while True:
    command = input()
    if command == 'exit' or command == 'quit':
        # todo: kill thread
        break
    if command == 'sendtest':
        utils.send(sock, 'MESSAGE' + json.dumps({'name': 'messages.getDialogs', 'useToken': True, 'args': ['count=1']}))
    else:
        if command != '':
            utils.send(sock, command)

# print(utils.read(sock))
print('Shutting down...')
sock.close()

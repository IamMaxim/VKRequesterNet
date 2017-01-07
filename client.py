import os
import socket
import ssl
import utils
import vkapi
import json
import threading
import time

vk = vkapi.VKApi(open('access_token.txt').read().strip('\n'))


def processMessage(msg):
    obj = json.loads(msg)
    print('response:', vk.sendRequest(obj['name'], obj['useToken'], obj['args']))


def startListening():
    while True:
        # read message from server
        res = utils.read(sock)
        print(res)
        if res == '' or res == 'err' or res == 'STOP':
            print('Server closed connection')
            sock.close()
            os._exit(0)
        if res.startswith('MESSAGE'):
            # remove MESSAGE and process
            processMessage(res[7:])

try:
    addr = open('address.txt', 'r').readline().split(':')
except FileNotFoundError:
    print('File "address.txt" not found. Can\'t connect.')
    raise SystemExit(0)
sock = ssl.wrap_socket(socket.socket())
sock.connect((addr[0], int(addr[1])))
# start listener thread
threading.Thread(target=startListening).start()
while True:
    command = input()
    if command == 'exit' or command == 'quit':
        # todo: kill thread
        break
    if command == 'sendtest':
        id = '151657174'
        utils.send(sock, 'MESSAGE' + json.dumps({'name': 'messages.send', 'useToken': True, 'args': ['message=%28%28%28', 'user_id=' + id]}))
        time.sleep(0.4)
        utils.send(sock, 'MESSAGE' + json.dumps({'name': 'messages.send', 'useToken': True, 'args': ['message=%29%29%29', 'user_id=' + id]}))
        time.sleep(0.4)
        utils.send(sock, 'MESSAGE' + json.dumps({'name': 'messages.send', 'useToken': True, 'args': ['message=%7C%7C%7C', 'user_id=' + id]}))
        time.sleep(0.4)
        utils.send(sock, 'MESSAGE' + json.dumps({'name': 'messages.send', 'useToken': True, 'args': ['message=%5C%7C%2F', 'user_id=' + id]}))
        time.sleep(0.4)
        utils.send(sock, 'MESSAGE' + json.dumps({'name': 'messages.send', 'useToken': True, 'args': ['message=%2F%7C%5C', 'user_id=' + id]}))
    else:
        if command != '':
            utils.send(sock, command)

# print(utils.read(sock))
print('Shutting down...')
sock.close()

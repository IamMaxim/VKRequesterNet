import urllib.request

class vkapi:
    def __init__(self, token):
        self.token = token

    def sendRequest(self, name, useToken, args):
        req = 'https://api.vk.com/method/' + name + "?v=5.60"
        if useToken:
            req += '&access_token=' + self.token
        for arg in args:
            req += '&' + arg
        req = req.replace(' ', '%20').replace('\n', '')
        return self.sendRequestByURL(req)

    def sendRequestByURL(self, req):
        res = urllib.request.urlopen(req)
        return res.read().decode('utf8')

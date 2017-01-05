import json


class User:
    """
    :arg nick: str
    :arg login: str
    :arg passhash: str
    :arg permission: int

    :arg obj: json with args as described above

    permission:
        0 - normal user
        1 - can send messages and ^
        2 - can execute commands on server and ^
    """

    def __init__(self, **kwargs):
        if kwargs.__contains__('obj'):
            obj = kwargs['obj']
            self.nick = obj['nick']
            self.login = obj['login']
            self.passhash = obj['passhash']
            self.permission = obj['permission']
        else:
            self.nick = kwargs['nick']
            self.login = kwargs['login']
            self.passhash = kwargs['passhash']
            self.permission = kwargs['permission']

    def __str__(self):
        return json.dumps({'nick': self.nick, 'login': self.login, 'passhash': self.passhash, 'permission': self.permission})

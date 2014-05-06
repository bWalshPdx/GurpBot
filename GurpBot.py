import socket

class IRCClient:
    socket = None
    connected = False
    nickname = 'Brian_Chan'
    channels = ['#Brian_Chan']

    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('irc.freenode.net', 6667))
        self.send("NICK %s" % self.nickname)
        self.send("USER %(nick)s %(nick)s %(nick)s :%(nick)s" % {'nick':self.nickname})

        while True:
            buf = self.socket.recv(4096)
            lines = buf.split("\n")
            for data in lines:
                data = str(data).strip()

                if data == '':
                    continue
                print "I<", data

                # server ping/pong?
                if data.find('PING') != -1:
                    n = data.split(':')[1]
                    self.send('PONG :' + n)
                    if self.connected == False:
                        self.perform()
                        self.connected = True

                args = data.split(None, 3)
                if len(args) != 4:
                    continue
                ctx = {}
                ctx['sender'] = args[0][1:]
                ctx['type']   = args[1]
                ctx['target'] = args[2]
                ctx['msg']    = args[3][1:]

                # whom to reply?
                target = ctx['target']
                if ctx['target'] == self.nickname:
                    target = ctx['sender'].split("!")[0]

                # some basic commands
                if ctx['msg'] == 'Brian_Chan!':
                    self.say('That\'s meeeeeee! -_-', target)

                if 'Brian' in ctx['msg']:
                    self.say('I\'m Brian!', target)

                if 'Brian_Chan' in ctx['msg']:
                    self.say('Genki desu!', target)


    def send(self, msg):
        print "I>",msg
        self.socket.send(msg+"\r\n")

    def say(self, msg, to):
        self.send("PRIVMSG %s :%s" % (to, msg))

    def perform(self):
        #self.send("PRIVMSG R : Register <>")
        self.send("PRIVMSG R : Login <>")
        self.send("MODE %s +x" % self.nickname)
        for c in self.channels:
            self.send("JOIN %s" % c)
            # say hello to every channel
            self.say('hello friends!', c)

IRCClient()

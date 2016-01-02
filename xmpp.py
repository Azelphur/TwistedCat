from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence


class XMPPBot(MessageProtocol):
    def __init__(self, config):
        self.config = config

    def connectionMade(self):
        # send initial presence
        self.send(AvailablePresence())

    def connectionLost(self, reason):
        print "Disconnected!"

    def sendMsg(self, dest, message):
        reply = domish.Element((None, "message"))
        reply["to"] = dest
        reply["type"] = 'chat'
        reply.addElement("body", content=message)
        self.send(reply)

    def msg(self, message):
        split = message.split()
        if split[0].lower() in self.config['users']:
            self.sendMsg(split[0], message[message.find(' ')+1:])
        else:
            for dest in self.config['users']:
                self.sendMsg(dest, message)

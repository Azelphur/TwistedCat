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

    def msg(self, message):
        for dest in self.config['users']:
            print "sending to", dest
            reply = domish.Element((None, "message"))
            reply["to"] = dest
            reply["type"] = 'chat'
            reply.addElement("body", content=message)
            self.send(reply)

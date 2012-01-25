from twisted.words.protocols import irc
from twisted.internet import protocol

class MomBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)
	self.factory.irc = self

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        print msg

class MomBotFactory(protocol.ClientFactory):
    protocol = MomBot

    def __init__(self, channel, nickname='`TheServer'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

    def sendmsg(self, message):
         self.irc.msg(self.channel, message)

from twisted.words.protocols import irc
from twisted.internet import protocol

class IRCBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.config['nick']
    nickname = property(_get_nickname)

    def _get_username(self):
        return self.factory.config['user']
    username = property(_get_username)

    def _get_realname(self):
        return self.factory.config['realname']
    realname = property(_get_realname)

    def _get_password(self):
        return self.factory.config['pass']
    password = property(_get_password)

    def _get_lineRate(self):
        return self.factory.config['lineRate']
    lineRate = property(_get_lineRate)

    versionName = "TwistedCat"

    def signedOn(self):
        for channel in self.factory.config['channels']:
            if self.factory.config['channels'][channel] and self.factory.config['channels'][channel].has_key('key'):
                self.join(channel, self.factory.config['channels'][channel]['key'])
            else:
                self.join(channel)

        print "Signed on as %s." % (self.nickname,)
        self.factory.irc = self

    def joined(self, channel):
        print "Joined %s." % (channel,)

class IRCBotFactory(protocol.ClientFactory):
    protocol = IRCBot

    def __init__(self, config):
        self.config = config

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

    def msg(self, message):
        split = message.split()
        if split[0] in self.config['channels'] or split[0] in self.config['users']:
            print "Sending message to", split[0]
            self.irc.msg(split[0], message[message.find(' ')+1:])
        else:
            for dest in self.config['channels']:
                self.irc.msg(dest, message)
            for dest in self.config['users']:
                self.irc.msg(dest, message)

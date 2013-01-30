from twisted.words.protocols import irc
from twisted.internet import protocol, ssl
import platform, socket, getpass
from twisted.internet.error import ConnectionLost

class IRCBot(irc.IRCClient):
    
    usage_message = None

    def _get_appname(self):
        return self.factory.APP_NAME
    versionName = property(_get_appname)

    def _get_appversion(self):
        return self.factory.APP_VERSION
    versionNum = property(_get_appversion)

    def _get_appurl(self):
        return self.factory.APP_URL
    sourceURL = property(_get_appurl)

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

    def _get_heartbeatInterval(self):
        if 'heartbeatInterval' in self.factory.config:
            return self.factory.config['heartbeatInterval']
        return 120.0 # this is the default per API docs
    heartbeatInterval = property(_get_heartbeatInterval)

    def signedOn(self):
    	for channel in self.factory.config['channels']:
		if self.factory.config['channels'][channel] and self.factory.config['channels'][channel].has_key('key'):
        		self.join(channel, self.factory.config['channels'][channel]['key'])
		else:
        		self.join(channel)
        print "Signed on as %s." % (self.nickname,)
	self.factory.irc = self
        print dir(self)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    """This will get called when the bot receives a message."""
    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            print "RECEIVED from %s on %s: %s" % (user, channel, msg,)
            msg = "%s: I am a bot. Send '%s?' for what little I know about the world." % (user, self.nickname)
            self.msg(channel, msg)
        elif msg.startswith(self.nickname + "?"):
            print "RECEIVED from %s on %s: %s" % (user, channel, msg,)
            msg = self.factory.usage_msg
            self.msg(channel, msg)

    def _onError(self, failure):
        print 'Failure %s at %s' % (failure, self.__class__.__name__)
        error = failure.trap(ConnectionLost)
        if error == ConnectionLost:
            # Do some beautiful things
            print 'Connection is lost. I want to reconnect NOW'
            print failure
        return failure

    def clientConnectionLost(self, connector, reason):
        print "client connection lost. reason: %s" % reason
        irc.IRCClient.clientConnectionLost(connector, reason)

    def connectionLost(self, reason):
        print "connection lost. reason: %s" % reason
        irc.IRCClient.connectionLost(self, reason)

    def clientConnectionFailed(self, connector, reason):
        print "connection failed. reason: %s" % reason
        irc.IRCClient.clientConnectionFailed(connector, reason)

    def irc_PING(self, prefix, params):
        print "IRC ping. prefix: %s params %s" % (prefix, params)

class IRCBotFactory(protocol.ClientFactory):
    protocol = IRCBot
    usage_msg = None

    def __init__(self, config, APP_VERSION, APP_NAME, APP_URL, VERBOSE):
        self.config = config
        self.APP_VERSION = APP_VERSION
        self.APP_NAME = APP_NAME
        self.APP_URL = APP_URL
        self.VERBOSE = VERBOSE
        hostname = socket.gethostbyname(platform.uname()[1])
        username = getpass.getuser()
        self.usage_msg = "%s v%s <%s> (running on %s (%s) as %s)" % (APP_NAME, APP_VERSION, APP_URL, hostname, platform.uname()[1], username)
        print dir(self)

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        protocol.ClientFactory.clientConnectionLost(connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
        protocol.ClientFactory.clientConnectionFailed(connector, reason)

    def msg(self, message, channels = None, users = None):
        if self.VERBOSE:
            print "IRCBotFactory.message(%s, %s, %s)" % (message, channels, users)
        # @TODO - for x in y works badly on strings. we need to somehow make sure these are treated as lists.
        if channels is None:
            channels = self.config['default_channels']
            if self.VERBOSE:
                print "IRCBotFactory.msg() setting channels to default"
        for dest in channels:
            if self.VERBOSE:
                print "IRCBotFactory call self.irc.msg(%s, %s)" % (dest, message)
            self.irc.msg(dest.encode('utf-8'), message.encode('utf-8'))
        if users is None:
            users = self.config['default_users']
            if self.VERBOSE:
                print "IRCBotFactory.msg() setting users to default"
        for dest in users:
            if self.VERBOSE:
                print "IRCBotFactory call self.irc.msg(%s, %s)" % (dest, message)
            self.irc.msg(dest.encode('utf-8'), message.encode('utf-8'))

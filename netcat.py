from twisted.protocols.basic import LineReceiver
from twisted.internet import protocol

class NetcatProtocol(LineReceiver):
    delimiter = "\n"

    def lineReceived(self, line):
	# Netcat message recieved
        line = line.rstrip("\r") # Apparently some systems send \r\n, so we're being safe.
        self.factory.message(line)

class NetcatFactory(protocol.ServerFactory):
    # Netcat factory to spawn NetcatProtocol instances
    protocol = NetcatProtocol

    def __init__(self, **kwargs):
        self.xmpp = kwargs['irc']

    def message(self, message):
        self.xmpp.sendmsg(message)

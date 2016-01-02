from twisted.protocols.basic import LineReceiver
from twisted.internet import protocol

class NetcatProtocol(LineReceiver):
    delimiter = "\n"

    def lineReceived(self, line):
        # Netcat message recieved
        line = line.rstrip("\r") # Apparently some systems send \r\n, so we're being safe.
        self.factory.message(line)
        self.transport.loseConnection()

class NetcatFactory(protocol.ServerFactory):
    # Netcat factory to spawn NetcatProtocol instances
    protocol = NetcatProtocol

    def __init__(self, **kwargs):
        self.connections = kwargs['factories']

    def message(self, message):
        for connection in self.connections:
            connection.msg(message)

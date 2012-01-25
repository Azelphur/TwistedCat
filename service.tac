from twisted.application import service, internet
from twisted.internet import reactor

# This is the IRC handler
from irc import MomBotFactory

# This is the Netcat handler
from netcat import NetcatProtocol, NetcatFactory

# IRC Server/Channel
CHANNEL='#test'
IRC_SERVER='irc.azelphur.com'
IRC_PORT=6667
NICK='TheServer'

# Port to listen on for netcat connections
PORT = 1079

# Create the application
application = service.Application("ircnetcat")

ircfactory = MomBotFactory(CHANNEL, NICK)
internet.TCPClient(IRC_SERVER, IRC_PORT, ircfactory).setServiceParent(service.IServiceCollection(application))

# Listen for netcat connections
factory = NetcatFactory(irc=ircfactory)
internet.TCPServer(PORT, factory).setServiceParent(service.IServiceCollection(application))

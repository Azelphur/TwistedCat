TwistedCat
==========

TwistedPrism is a Python/Twisted daemon to handle syndication of notifications
from and to multiple sources and destinations (mainly chat services). It's
intended to be a funnel for your various notifications into an IRC channel or
XMPP chat. It currently listens for either netcat (string-over-a-socket) or
HTTP (GET url params or form-encoded POST data) requests, and relays a simple
string from the input to an output (one or more IRC or XMPP channels/chats). 

This project is intended to provide an easy way to take simple string messages
from "things" that you want to know about (monitoring system alerts, tickets
or bug reports, CI/CD system job status, administrative tools, etc.) and allow
them to be broadcast into IRC or XMPP channels (or perhaps more outputs in the
future) with no more than a HTTP GET or POST, a simple string write to a
socket, or echoing to `netcat` in a shell script. 

At this time, the design sends all incoming traffic to all outputs and relies
on the consumers to filter or highlight as desired, based on the contents of
the message. If totally separate flows are desired, multiple instances of
TwistedCat can be spun up on different ports.

Inputs
------
* netcat (string-over-a-socket)
* HTTP GET or POST

Outputs
-------
* IRC channel and/or user (multiple of each)
* XMPP/Jabber - direct user messaging only, no chats

Usage - Server
--------------
# Copy `config.cfg.example` to `config.cfg` and edit as necessary for your
environment. Remove any sections you don't want. Each client section
supports multiple accounts, meaning you can have the bot on multiple IRC
networks, or multiple XMPP accounts.
# Start the bot with `twistd -y twistedcat.tac`
# If you have any issues, keep it in the foreground with `twistd -n -y twistedcat.tac`

Usage - Clients
---------------
* Send string data to the server on the port used for netcat
(netcat.port). `echo "Hello World" | nc localhost 1079`, or the equivalent
socket code in the language of your choice.
* Send a string via HTTP to the server. This can be either a HTTP POST of form
encoded data to `/notification/send`, with the string in a "message" argument,
or it can be via a GET where the message is URL encoded as a parameter, of the
form `/notification/send?message=foo%20bar%20baz`. 
* At some point I plan on implementing some sort of very basic accidental
message storm protection - it will likely be a key sent in plaintext with the
data, checked against a plaintext database (hence why I can't even call it
security; the only real purpose will be to make it less likely that someone
will accidentally stumble upon the URL and start spamming the bot, and to have
a way to filter out rogue devices that are pushing messages). This will likely
be done for HTTP but *not* netcat, so I recommend using the HTTP interface
wherever possible.

Acknowledgements
----------------

The code I began working on was a GitHub repo forked from that of Azelphur
Gaming [TwistedCat](https://github.com/Azelphur/TwistedCat). He in turn says
that the IRC protocol class came from [Eric Florenzano's Blog
post](http://eflorenzano.com/blog/2008/11/16/writing-markov-chain-irc-bot-twisted-and-python/).

License
-------
Unknown. Neither of the two people whose code has gone into this published
notice of a specific license for their work. I'd like to say 'something along
the spirit of the GPLv3'. Or, in more concrete terms, do whatever you want
with this so long as you make every effort to send changes/improvements back
to me (ideally by forking the repository and sending a pull request), 
report any bugs that you find, and keep author/contributor information intact.

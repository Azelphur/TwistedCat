from twisted.internet import protocol
from twisted.web import server, resource, http
import json
from logging import TwistedPrismLogging as tpl

# from http://nullege.com/codes/show/src%40p%40l%40planes-HEAD%40twisted_serve.py/6/twisted.web.http.HTTPChannel/python
class MyHttpRequest(http.Request):
  
    def process(self):
        if self.method == "POST":
	    print "POST from %s to %s: %s" % (self.getClientIP(), self.uri, self.content.getvalue())
            self.args = json.loads(self.content.getvalue())
            foo = self.args['message']
            self.args['message'] = []
            self.args['message'].append(foo)
        # self.responseHeaders type is http_headers.Headers
        self.setHeader("Server", "%s v%s (%s)" % (self.channel.factory.GLOBAL_CONF['APP_NAME'], self.channel.factory.GLOBAL_CONF['APP_VERSION'], self.channel.factory.GLOBAL_CONF['APP_URL']))
        # self.getHeader(key) returns bytes or NoneType
        # self.getAllHeaders() - returns a dict of all response headers
        if self.path == "/notification/send":
            if self.channel.factory.GLOBAL_CONF['logging']['verbosity'] >= tpl.L_DEBUG:
                print "MyHttpRequest.process() self.args: %s" % self.args
            channels = None
            users = None
            if "channels" in self.args:
                channels = self.args['channels']
            if "users" in self.args:
                users = self.args['users']
            if "message" in self.args:
                self.channel.factory.message(self.args['message'][0], channels, users)
                self.setResponseCode(202, message="Message passed to notifiers.")
                self.write("message passed to notifiers")
            else:
                self.setResponseCode(400, message="message not specified")
        else:
            self.setResponseCode(404, message="invalid path")
        self.finish() # this also writes out an access log line

class Channel(http.HTTPChannel):
    requestFactory = MyHttpRequest
    

class HTTPServerFactory(http.HTTPFactory):

    protocol = Channel
    _logDateTimeCall = None

    def __init__(self, config, GLOBAL_CONF, **kwargs):
        self.config = config
        self.GLOBAL_CONF = GLOBAL_CONF
        self.connections = kwargs['factories']

    def message(self, message, channels = None, users = None):
	for connection in self.connections:
            if self.GLOBAL_CONF['logging']['verbosity'] >= tpl.L_DEBUG:
                print "HTTPServerFactory.message(%s, %s, %s)" % (message, channels, users)
            connection.msg(message, channels, users)

from twisted.internet import protocol
from twisted.web import server, resource, http

# from http://nullege.com/codes/show/src%40p%40l%40planes-HEAD%40twisted_serve.py/6/twisted.web.http.HTTPChannel/python
class MyHttpRequest(http.Request):
  
    def process(self):
        if self.method == "POST":
	    print "POST args from %s at %s: %s" % (self.getClientIP(), self.uri, self.args)
        # self.responseHeaders type is http_headers.Headers
        # self.setHeader(name, value)
        # self.getHeader(key) returns bytes or NoneType
        # self.getAllHeaders() - returns a dict of all response headers
	if "message" in self.args:
	    self.channel.factory.message(self.args['message'][0])
	    self.setResponseCode(202, message="Message passed to notifiers.")
	    self.write("message passed to notifiers")
	else:
	    self.setResponseCode(400, message="message not specified")
        self.finish() # this also writes out an access log line

class Channel(http.HTTPChannel):
    requestFactory = MyHttpRequest
    

class HTTPServerFactory(http.HTTPFactory):

    protocol = Channel
    _logDateTimeCall = None

    def __init__(self, config, **kwargs):
        self.config = config
        self.connections = kwargs['factories']

    def message(self, message):
	for connection in self.connections:
		connection.msg(message)
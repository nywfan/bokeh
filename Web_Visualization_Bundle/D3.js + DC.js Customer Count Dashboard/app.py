# Webserver stuff
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options

# Utility libraries
import os.path
import logging
from socket import gethostbyname, gethostname

# logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# options
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    """ main server template """
    def __init__(self):
        handlers = [(r"/", MainHandler)]
                    
        # debug=True, testing mode
        # Tornado will attempt to restart the server each time the main Python file is modified, and refresh templates as they change. 
        # Do not leave it on in production, because it prevents Tornado from caching templates
        
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                gzip=True,
                debug=True
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    """base class for all requests"""
    def _handle_request_exception(self, e):
        self.render('error.html',
                    main_title = 'D3.js + DC.js Customer Count Dashboard',
                    err = str(e)
        )

class MainHandler(BaseHandler):
    def get(self):
        try:
            self.render('index.html',
                        main_title = 'D3.js + DC.js Customer Count Dashboard'
            ) 
        except Exception as e:
            logger.error(e)
            logger.debug(self._handle_request_exception(str(e)))     


# Start the server at port n
if __name__ == "__main__":
    tornado.options.parse_command_line()
    host_ip = gethostbyname(gethostname())
    msg = '\n\n' + r'Server Running at http://localhost:' + str(options.port) + r'/' + '\n\n' + 'HostName: ' + gethostname() + '\n\n' + 'Host IP: ' + host_ip + '\n\n' + r'To close press ctrl + c'
    logger.info(msg)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)    
    tornado.ioloop.IOLoop.instance().start()



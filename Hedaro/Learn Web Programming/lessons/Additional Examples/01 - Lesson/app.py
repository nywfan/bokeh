# Webserver stuff
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

# Utility libraries
import os
import os.path
import logging

# logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# options
define("port", default=8888, help="run on the given port", type=int)  
define("debug", default=True, type=bool)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", Home)]
                    
        """
        # debug=True, testing mode
        # Tornado will attempt to restart the server each time the main Python file is modified, and refresh templates as they change. 
        # Do not leave it on in production, because it prevents Tornado from caching templates
        """
        
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                gzip=True,
                debug=options.debug
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)     
        

class BaseHandler(tornado.web.RequestHandler):
    """base class for all requests"""
    def _handle_request_exception(self, e):
        logger.info(str(e))
        self.write('error')
        

class Home(BaseHandler):
    def get(self):
        self.render('index.html',
                    main_title = '02 - Lesson'
        )        
    

# Script start here
if __name__ == "__main__":
    tornado.options.parse_command_line()
    msg = '\n\n' + r'Server Running at http://localhost:' + str(options.port) + r'/' + '\n\n' + r'To close press ctrl + c'
    logger.info(msg)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)    
    tornado.ioloop.IOLoop.instance().start()
    
    
# Webserver stuff
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

# Utility libraries
import re
import os
import os.path
import logging

# logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# options
define("port", default=8888, help="run on the given port", type=int)  
define("debug", default=True, type=bool)

def validate(field, regex):
    """ checks sure form input """
    if re.match(regex, field, re.VERBOSE):
        return True
    else:
        return False

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", Home)]
        
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                gzip=True,
                debug=options.debug
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)     
        

class BaseHandler(tornado.web.RequestHandler):
    """ base class for all requests """
    def _handle_request_exception(self, e):
        logger.info(str(e))
        self.write('error')
        
class Home(BaseHandler):
    def get(self):
        self.render('index.html',
                    main_title = '02 - Lesson'
        )        

    def post(self):
        # get parameters
        userfirstname = self.get_argument('userfirstname', None)
        userlastname = self.get_argument('userlastname', None)
            
        # server-side validation    
        # any alpha (upper or lower case) character that is between 2 and 60 characters long
        if (userfirstname and validate(userfirstname, "^[A-Za-z]{2,60}$") and             
			userlastname and validate(userlastname, "^[A-Za-z]{2,60}$")):    
			
            self.render('success.html',
                        main_title = '02 - Lesson',
                        first = userfirstname,
                        last = userlastname
            )
   
        else:
              
            self.render('error.html',
                        main_title = '02 - Lesson',
                        err = 'I am sorry, we are having issues processing your request'
            )	

if __name__ == "__main__":
    """ Script start here """
    tornado.options.parse_command_line()
    msg = '\n\n' + r'Server Running at http://localhost:' + str(options.port) + r'/' + '\n\n' + r'To close press ctrl + c'
    logger.info(msg)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)    
    tornado.ioloop.IOLoop.instance().start()
    
    
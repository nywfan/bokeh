# Webserver stuff
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.options import define, options

# Utility libraries
import os
import os.path
import logging
import datetime
from socket import gethostbyname, gethostname
import time
import json

# Scripts
import common as comm
import git_catalog as git

# logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# options
define("port", default=8888, help="run on the given port", type=int)  
define("debug", default=True, type=bool)

# variables
title = 'Python Reporting Server'

# functions
def load_config(filename):
    """loads settings"""
    with open(filename,'r')	 as f:
        return json.loads(f.read())
        
def update_config(repo):
    """update settings"""
    
    err = True
    
    try:    
        jsonFile = load_config('config.json') # load json
        data = jsonFile                       # make copy
        #jsonFile.close()                      # close json
    
        # update json
        data["repo_location"] = repo
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
    except Exception as e:
        err = None
        logger.error(e)         

    return err


class Application(tornado.web.Application):
    """ main """

    def __init__(self):
        handlers = [(r"/", Home),
                    (r"/error", Error),
                    (r"/faq", Faq),
                    (r"/url", URL),
                    (r"/nbupdate", nbUPDATE),
                    (r"/settings", nbSettings),                    
                    (r"/.*", NotFound)]
                    
        # debug=True, testing mode
        # Tornado will attempt to restart the server each time the main Python file is modified, and refresh templates as they change. 
        # Dont leave it on in production, because it prevents Tornado from caching templates
        
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                gzip=True,
                debug=True
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)
      


class BaseHandler(tornado.web.RequestHandler):
    """ base class for all requests """
    def _handle_request_exception(self, e):
        self.render('error.html',
                    main_title = title,
                    err = e
        )	


class Home(BaseHandler):
    """ index page """
    def get(self):
    
        svnCatalog = None # initialize variable
        
        try:
            conf = load_config('config.json')  
            repo = conf['repo_location']
            svnCatalog = comm.to_HTML(git.git_get(repo))
        except Exception as e:
            logger.error(e)
            #logger.debug(self._handle_request_exception(str(e)))
        finally:
            if svnCatalog:
                self.render('catalog.html',
                            main_title = title,
                            tbl = svnCatalog
                ) 
            else:                
                self.render('error.html',
                            main_title = title,
                            err = "Go to Settings and enter a valid GIT repository."
                )            

class Error(BaseHandler):
    """ default page for errors """
    def get(self):
        self.render('error.html',
                    main_title = title,
                    err = ''
        )            	


class Faq(BaseHandler):
    """ FAQ page """
    def get(self):
        self.render('faq.html',
                    main_title = title
        ) 	                  

class URL(BaseHandler):		
    """ notebook HTML parser """		
    def get(self):
        # cmd type
        # setx svnpass enterpasswordhere
        # setx svnuser enterusernamehere
        # to remove setx entervariablenamehere ""
        
        # get parameters
        nburl = self.get_argument('nburl', False)
        showcode = self.get_argument('showcode', False)
        render = self.get_argument('render', 'html')
        
        try:
            html = comm.Viewer(nburl=nburl, showcode=showcode, render=render)
            self.render('myview.html',
                        main_title = title,
                        data = html
            )	 
        except Exception as e:
            logger.error(e)
            logger.debug(self._handle_request_exception(str(e)))        
        

class nbUPDATE(BaseHandler):		
    """ checkout, run, save, and commit """		
    @tornado.web.asynchronous
    @tornado.gen.coroutine          
    def post(self):
        burl = self.get_argument('burl', False)
        nburl = self.get_argument('nburl', False)        
        fn = self.get_argument('fn', False)
        
        try:
            html = git.nb_update(repo_path=burl, fpath=nburl, fname=fn, msg='BARS - manual update')
        except Exception as e:
            logger.error(e)
            logger.debug(self._handle_request_exception(str(e)))  

    get = post         

    
class NotFound(BaseHandler):
    """ default page for unknown urls """
    def get(self):
        self.render('notfound.html',
            main_title = title
        )
        
class nbSettings(BaseHandler):
    """ Settings page """    
    
    def get(self):

        conf = load_config('config.json')   # get data
        repo_loc = conf['repo_location']    # get new repo location    
    
        # switch between production and development
        if options.debug:
            actionurl = r'/settings'
        else:
            actionurl = r'http://fastforms.herokuapp.com/signup' 
        
        self.render('settings.html',
                    main_title = title,
                    action = actionurl,
                    repo = repo_loc
        )

    def post(self):
    
        # initialize parameters
        result = None
        svnCatalog = None
        repo = self.get_argument('repo', None)       

        # Start validation sections
        if repo:
            try:
                result = update_config(repo)        # update repo
                conf = load_config('config.json')   # get data
                repo_loc = conf['repo_location']    # get new repo location
            except Exception as e:
                logger.error(e)
                logger.debug(self._handle_request_exception(str(e)))         
            finally:
                if result:
                    try:
                        svnCatalog = comm.to_HTML(git.git_get(repo_loc))
                    except Exception as e:
                        logger.error(e)
                        #logger.debug(self._handle_request_exception(str(e))) 
                    finally:
                        if svnCatalog:
                            self.render('catalog.html',
                                        main_title = title,
                                        tbl = svnCatalog
                            ) 
                        # invalid repo path
                        else:                
                            self.render('error.html',
                                        main_title = title,
                                        err = "Go to Settings and enter a valid GIT repository."
                            )
                # repo update failed
                else:                
                    self.render('error.html',
                                main_title = title,
                                err = "I'm sorry, there was an error updating your repository location."
                    )   
        # form did not return a value            
        else:                
            self.render('error.html',
                        main_title = title,
                        err = "I'm sorry, you did not enter a repository location"
            )                       
          
        
        

# Start the server at port n
if __name__ == "__main__":
    tornado.options.parse_command_line()
    host_ip = gethostbyname(gethostname())
    msg = '\n\n' + r'Server Running at http://localhost:' + str(options.port) + r'/' + '\n\n' + 'HostName: ' + gethostname() + '\n\n' + 'Host IP: ' + host_ip + '\n\n' + r'To close press ctrl + c'
    logger.info(msg)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)    
    tornado.ioloop.IOLoop.instance().start()
    
    
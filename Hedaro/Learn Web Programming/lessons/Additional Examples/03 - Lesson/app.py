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

# Sqlalchemy imports
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import scoped_session, sessionmaker

# Scripts
import models
from script import gentbl

# options
define("port", default=8888, help="run on the given port", type=int)  
define("debug", default=True, type=bool)
define("db_path", default='sqlite:///tutorial.db', type=str)

def validate(field, regex):
    """ checks sure form input """
    if re.match(regex, field, re.VERBOSE):
        return True
    else:
        return False

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", Home),
                    (r"/db", DB)]
        
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                gzip=True,
                debug=options.debug
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)     
        
        # Have one global connection.
        engine = create_engine(options.db_path, convert_unicode=True, echo=False)
        models.init_db(engine)
        self.db = scoped_session(sessionmaker(bind=engine))          
        

class BaseHandler(tornado.web.RequestHandler):
    """base class for all requests"""
    def _handle_request_exception(self, e):
        logger.info(str(e))
        self.write('error')
        
    @property
    def db(self):
        return self.application.db       

class DB(BaseHandler):
    """ select all records from database """
    def get(self):        
    
        try:
            data = self.db.query(models.UserModel).all()
            
            # loop through data and place the results into a list
            rec = []
            for x in data:
                rec.append((x.firstname, x.lastname)) 
                
        except Exception as e:
            logger.error(e)
            logger.debug('get records from DB failed')
            data = None
        finally:
            self.db.close() 
        
        # if we found records in the database
        if data:    
        
            # run the gentbl function
            try:
                result = gentbl(rec)
            except Exception as e:
                logger.error(e)
                logger.debug('failed to run gentbl function')
                result = None
                raise e   
            
            if result:    
                # render the html table
                self.render('db.html',
                            main_title = '03 - Lesson',
                            table = result
                )               

            else:
                # return generic error msg  
                self.render('error.html',
                            main_title = '03 - Lesson',
                            err = 'I am sorry, we are having issues processing your request'
                )	            
          
        # database was either empty or there was an issue with the query 
        else:
              
            self.render('error.html',
                        main_title = '03 - Lesson',
                        err = 'I am sorry, we are having issues processing your request'
            )	             
            
        
class Home(BaseHandler):
    def get(self):
        self.render('index.html',
                    main_title = '03 - Lesson'
        )        

    def post(self):
        userfirstname = self.get_argument('userfirstname', None)
        userlastname = self.get_argument('userlastname', None)
            
        if (userfirstname and validate(userfirstname, "^[A-Za-z]{2,60}$") and             
			userlastname and validate(userlastname, "^[A-Za-z]{2,60}$")):    
            
            # If validation passes, insert records into DB
            try:
                userModel = models.UserModel(firstname = userfirstname,
                                             lastname = userlastname)
                self.db.add(userModel)
                self.db.commit()
            except Exception as e:
                logger.error(e)
                logger.debug('save to db failed')
                self.db.rollback()
            finally:
                self.db.close()             
            
			
            self.render('success.html',
                        main_title = '03 - Lesson',
                        first = userfirstname,
                        last = userlastname
            )
   
        else:
            # validation failed  
            self.render('error.html',
                        main_title = '03 - Lesson',
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
    
    
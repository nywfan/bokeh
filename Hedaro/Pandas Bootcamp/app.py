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
import numpy as np
import pandas as pd
from numpy import random

# Scripts
import questions as q


# logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# options
define("port", default=8888, help="run on the given port", type=int)  
define("debug", default=True, type=bool)

# variables
title = 'Pandas Bootcamp'

class Application(tornado.web.Application):
    """ main """

    def __init__(self):
        handlers = [(r"/", Home),
                    (r"/error", Error),
                    (r"/faq", Faq),                   
                    (r"/.*", NotFound)]
        
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
        
        s, d = q.pd_create_dataset()             # create seed and dataframe  
        rawtbl = q.pd_create_table(s, d)         # create html table
        questions = q.pd_create_questions(d)     # create questions and answers         
        #pd.DataFrame(d).to_clipboard()           # copy dataframe to clipboard

        # pool of questions
        pool = questions['id'].values
        
        # pick random question from pool
        qid = pool[random.randint(low=0,high=len(pool))]
        
        # get question id
        # get question text
        mask = questions['id'] == qid
        questionname = questions['question'][mask].values        

        # switch between production and development
        if options.debug:
            actionurl = r'/'
        else:
            actionurl = r'/' 

        self.render('index.html',
                    main_title = title,
                    qname = str(questionname[0]),
                    action = actionurl,
                    data = d,
                    tbl = rawtbl,
                    seed = s,
                    id = qid
        )    

    @tornado.web.asynchronous
    @tornado.gen.coroutine          
    def post(self):
        
        # get parameters
        data = json.loads(self.request.body)
        data2 = data['new_data'] 

        try:
            # re-create questions and answers
            s, d = q.pd_create_dataset(seed = int(data2['useed']))  
            questions = q.pd_create_questions(df = d)
            mask = questions['id'] == int(data2['uid'])
            sans = questions['ans'][mask].values
            #print sans
            
            # check id user answer is correct
            # round to 2 decimal places
            if (len(data2['uans']) > 0 and round(float(data2['uans']), 2) == round(float(sans), 2)):
                result={'user':data2['uans'], 'sys':float(sans),'result':True}  
            else:
                result={'user':data2['uans'], 'sys':float(sans),'result':False}

            # push results back to the front-end
            self.write(json.dumps(result))    
                
        except Exception as e:
            logger.error(e)
            logger.debug(self._handle_request_exception(str(e)))         
        

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

    
class NotFound(BaseHandler):
    """ default page for unknown urls """
    def get(self):
        self.render('notfound.html',
            main_title = title
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
    
    
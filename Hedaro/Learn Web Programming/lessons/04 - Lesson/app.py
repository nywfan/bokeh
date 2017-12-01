# Webserver stuff
import tornado.ioloop
import tornado.web


# Utility libraries
import os.path


# route to index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
                    page_title = 'This is Amazing!!!',
                    page_heading = 'Welcome to Tornado',
                    company_name = 'Business Intelligence'
        ) 


settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
)


# r"/" == root website address
application = tornado.web.Application([
    (r"/", MainHandler)
],**settings) 


# Start the server at port n
if __name__ == "__main__":
    PortNumber = str(8888)
    print r'Server Running at http://localhost:' + PortNumber + r'/'
    print r'To close press ctrl + c'
    application.listen(PortNumber)
    tornado.ioloop.IOLoop.instance().start()



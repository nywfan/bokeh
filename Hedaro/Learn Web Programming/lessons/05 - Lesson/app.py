# Webserver stuff
import tornado.ioloop
import tornado.web


# User created scripts
from JsonExample import to_json
from HtmlTblExample import html


# Utility libraries
import os.path


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
                    page_title = 'This is Amazing!!!',
                    company_name = 'Business Intelligence',
                    tbl = html()
        ) 

class welcome(tornado.web.RequestHandler):
    def get(self):
        self.render('welcome.html',
                    page_title = 'This is Amazing!!!',
                    company_name = 'Business Intelligence'
        )

class data(tornado.web.RequestHandler):
    def get(self):
        self.write(to_json())

class data2(tornado.web.RequestHandler):
    def get(self):
        self.write(html())
        

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
)

# r"/" == root website address
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/welcome", welcome),
    (r"/data", data),
    (r"/data2", data2)
],**settings) 


# Start the server at port n
if __name__ == "__main__":
    PortNumber = str(8888)
    print r'Server Running at http://localhost:' + PortNumber + r'/'
    print r'To close press ctrl + c'
    application.listen(PortNumber)
    tornado.ioloop.IOLoop.instance().start()



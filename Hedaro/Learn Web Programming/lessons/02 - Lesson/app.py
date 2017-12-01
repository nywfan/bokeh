# Webserver stuff
import tornado.ioloop
import tornado.web


# route to index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html',
                    page_title = 'This is Amazing!!!',
                    page_heading = 'Welcome to Tornado'
        ) 


# r"/" == root website address
application = tornado.web.Application([
    (r"/", MainHandler)
],debug=True) 


# Start the server at port n
if __name__ == "__main__":
    PortNumber = str(8888)
    print r'Server Running at http://localhost:' + PortNumber + r'/'
    print r'To close press ctrl + c'
    application.listen(PortNumber)
    tornado.ioloop.IOLoop.instance().start()



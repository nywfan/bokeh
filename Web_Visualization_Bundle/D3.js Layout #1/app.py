# Webserver stuff
import tornado.ioloop
import tornado.web

# Utility libraries
import os.path


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

# This tells tornado where to find the static files
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
    print('Server Running...')
    print('Press ctrl + c to close')
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



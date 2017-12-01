# Webserver stuff
import tornado.ioloop
import tornado.web

# Utility libraries
import os.path


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lessons',
                    static_path = settings['static_path']
        )

class Lesson1(tornado.web.RequestHandler):
    def get(self):
        self.render('01 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 1'
        )

class Lesson2(tornado.web.RequestHandler):
    def get(self):
        self.render('02 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 2'
        )

class Lesson3(tornado.web.RequestHandler):
    def get(self):
        self.render('03 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 3'
        )

class Lesson4(tornado.web.RequestHandler):
    def get(self):
        self.render('04 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 4'
        )

class Lesson5(tornado.web.RequestHandler):
    def get(self):
        self.render('05 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 5'
        ) 

class Lesson6(tornado.web.RequestHandler):
    def get(self):
        self.render('06 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 6'
        ) 

class Lesson7(tornado.web.RequestHandler):
    def get(self):
        self.render('07 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 7'
        )

class Lesson8(tornado.web.RequestHandler):
    def get(self):
        self.render('08 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 8'
        )

class Lesson9(tornado.web.RequestHandler):
    def get(self):
        self.render('09 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 9'
        )

class Lesson10(tornado.web.RequestHandler):
    def get(self):
        self.render('10 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 10'
        )

class Lesson11(tornado.web.RequestHandler):
    def get(self):
        self.render('11 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 11'
        )

class Lesson12(tornado.web.RequestHandler):
    def get(self):
        self.render('12 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 12'
        ) 

class Lesson13(tornado.web.RequestHandler):
    def get(self):
        self.render('13 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 13'
        ) 

class Lesson14(tornado.web.RequestHandler):
    def get(self):
        self.render('14 - Lesson.html',
                    main_title = 'DC Rocks!!!',
                    page_title = 'Lesson 14'
        ) 

# This tells tornado where to find the static files
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
)

# r"/" == root website address
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/Lesson1", Lesson1),
    (r"/Lesson2", Lesson2),
    (r"/Lesson3", Lesson3),
    (r"/Lesson4", Lesson4),
    (r"/Lesson5", Lesson5),
    (r"/Lesson6", Lesson6),
    (r"/Lesson7", Lesson7),
    (r"/Lesson8", Lesson8),
    (r"/Lesson9", Lesson9),
    (r"/Lesson10", Lesson10),
    (r"/Lesson11", Lesson11),
    (r"/Lesson12", Lesson12),
    (r"/Lesson13", Lesson13),
    (r"/Lesson14", Lesson14)
],**settings) 

# Start the server at port n
if __name__ == "__main__":
    print 'Server Running...'
    print 'Press ctrl + c to close'
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



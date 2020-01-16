import request
import json
import tornado.ioloop
import tornado.web



def turnOnLights(court, time):
    return 0


def turnOffLights(court):
    return 0


def turnOnHeater(court, time):
    return 0


def turnOffHeater(court):
    return 0


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        court   = self.get_argument("court")
        service = self.get_argument("service")
        time    = self.get_argument("time"self.write("Your username is %s and password is %s" % (user, passwd))



def make_app():
    return tornado.web.Application([
        (r"/", HelloHandler),
    ])


def main():
    return 0



if __name__== "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()

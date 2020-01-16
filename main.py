import requests
import json
import tornado.ioloop
import tornado.web
import time, threading

HEATERS_GPIO = [1,2]
LIGHTS_GPIO = [3,4]

SERVICES = ['heater', 'lights']
TIMES = [15, 30, 45, 60, 75, 90, 105, 120]
COURTS = [1, 2]

TIMERS_LIGHTS = [None, None]
TIMERS_HEATER = [None, None]


def turnOnLights(court, time):
    global TIMERS_LIGHTS
    try:
        TIMERS_LIGHTS[court-1].cancel()
    except:
        print('Timer not active')
    TIMERS_LIGHTS[court-1] = threading.Timer(2, turnOffLights, [court]).start()
    print("turning on lights!")
    return 0


def turnOffLights(court):
    global TIMERS_LIGHTS
    TIMERS_LIGHTS[court-1].cancel()
    print("turning off lights of court %s", court)
    return 0


def turnOnHeater(court, time):
    global TIMERS_HEATER
    try: 
        TIMERS_HEATER[court-1].cancel()
    except:
        print('Timer not active')
    TIMERS_HEATER[court-1] = threading.Timer(2, turnOffHeater, [court]).start()
    print("turning heater")
    return 0


def turnOffHeater(court):
    global TIMERS_HEATER
    TIMERS_HEATER[court-1].cancel()
    print('tourning off heater of court %s', court)
    return 0


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        court   = int(self.get_argument("court"))
        service = str(self.get_argument("service"))
        time    = int(self.get_argument("time"))

        if not court in COURTS:
            self.write("Wrong court number, %s. Must be 1 or 2" % (court) )
            return -1

        if not service in SERVICES:
            self.write("Wrong service")
            return -2

        if not time in TIMES:
            self.write("Wrond time")
            return -3
    
        print(service)
        
        if service == "heater":
            turnOnHeater(court, time)

        if service == 'lights':
            turnOnLights(court, time)

        self.write("Turn on court %s %s for %s minutes." % (court, service, time))



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

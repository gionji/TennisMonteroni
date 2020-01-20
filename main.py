import requests
import json
import tornado.ioloop
import tornado.web
import time, threading
import subprocess


HEATERS_GPIO = [36,37]
LIGHTS_GPIO  = [38,39]
GPIO_PATH = "/gpio/pin"


SERVER_PORT = 8888

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
    
    TIMERS_LIGHTS[court-1] = threading.Timer(2, turnOffLights, [court])
    TIMERS_LIGHTS[court-1].start()
    
    turnOnGpio(LIGHTS_GPIO[court-1])
    print("turning on lights!")
    return 0


def turnOffLights(court):
    global TIMERS_LIGHTS
    TIMERS_LIGHTS[court-1].cancel()

    turnOffGpio(LIGHTS_GPIO[court-1])
    print("turning off lights of court %s", court)
    return 0


def turnOnHeater(court, time):
    global TIMERS_HEATER
    try: 
        TIMERS_HEATER[court-1].cancel()
    except:
        print('Timer not active')

    turnOnGpio(HEATERS_GPIO[court-1])
    
    TIMERS_HEATER[court-1] = threading.Timer(2, turnOffHeater, [court])
    TIMERS_HEATER[court-1].start()

    print("turning heater")
    return 0


def turnOffHeater(court):
    global TIMERS_HEATER
    TIMERS_HEATER[court-1].cancel()

    turnOffGpio(HEATERS_GPIO[court-1])
    print('tourning off heater of court %s', court)
    return 0


def setupGpio():
    #set lights gpio
    for gpioNumber in LIGHTS_GPIO:
        f = open(GPIO_PATH + str(gpioNumber) + "/direction", "w+")
        f.write("out")
        f.flush()
        f.close()

    for gpioNumber in HEATERS_GPIO:
        f = open(GPIO_PATH  + str(gpioNumber) + "/direction", "w+")
        f.write("out")
        f.flush()
        f.close()

   

def turnOnGpio(pcbNumber):
    f = open(GPIO_PATH + str(gpioNumber) + "/value", "w+")
    f.write("high")
    f.flush()
    f.close() 


def turnOffGpio(pcbNumber):
    f = open(GPIO_PATH + str(gpioNumber) + "/value", "w+")
    f.write("low")
    f.flush()
    f.close()
   



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
    setupGpio()
    return 0



if __name__== "__main__":
    main()
    app = make_app()
    app.listen(SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()

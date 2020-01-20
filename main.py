import requests
import json
import tornado.ioloop
import tornado.web
import time, threading
import subprocess
import argparse

HEATERS_GPIO = [36,37]
LIGHTS_GPIO  = [38,39]
GPIO_PATH = "/gpio/pin"


SERVER_PORT = 8888

SERVICES = ['heater', 'lights']
TIMES = [1,2, 5,15, 30, 45, 60, 75, 90, 105, 120]
COURTS = [1, 2]

TIMERS_LIGHTS = [None, None]
TIMERS_HEATER = [None, None]

SHORT_TIMER = False

def turnOnLights(court, time):
    global TIMERS_LIGHTS
    try:
        TIMERS_LIGHTS[court-1].cancel()
    except:
        print('Timer not active')

    TIMERS_LIGHTS[court-1] = threading.Timer(time, turnOffLights, [court])
    TIMERS_LIGHTS[court-1].start()
    
    turnOnGpio(LIGHTS_GPIO[court-1])
    print("LOG: Turning on lights. Court " + str(court) + " for " + str(time) + " seconds." )
    return 0


def turnOffLights(court):
    global TIMERS_LIGHTS
    TIMERS_LIGHTS[court-1].cancel()

    turnOffGpio(LIGHTS_GPIO[court-1])
    print("LOG: Turning off lights: court " + str(court) )
    return 0


def turnOnHeater(court, time):
    global TIMERS_HEATER
    try: 
        TIMERS_HEATER[court-1].cancel()
    except:
        print('Timer not active')

    turnOnGpio(HEATERS_GPIO[court-1])
    
    TIMERS_HEATER[court-1] = threading.Timer(time*60, turnOffHeater, [court])
    TIMERS_HEATER[court-1].start()

    print("LOG: Turning on heater. Court " + str(court) + " for " + str(time) + " seconds." )

    return 0


def turnOffHeater(court):
    global TIMERS_HEATER
    TIMERS_HEATER[court-1].cancel()

    turnOffGpio(HEATERS_GPIO[court-1])
    print('LOG: tourning off heater: court' + str(court))
    return 0


def setupGpio():
    #set gpio in output mode
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

def setupValues():
    turnOffGpio(36)   
    turnOffGpio(37)
    turnOffGpio(38)
    turnOffGpio(39)

def turnOnGpio(gpioNumber):
    f = open(GPIO_PATH + str(gpioNumber) + "/value", "w+")
    f.write("0")
    f.flush()
    f.close() 


def turnOffGpio(gpioNumber):
    f = open(GPIO_PATH + str(gpioNumber) + "/value", "w+")
    f.write("1")
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
            self.write("Wrong time")
            return -3
    
        if not SHORT_TIMER:
            time = time * 60
        
        if service == "heater":
            turnOnHeater(court, time)

        if service == 'lights':
            turnOnLights(court, time)

        self.write("Turn on court %s %s for %s seconds. (%s minutes)" % (court, service, time, time/60))



def make_app():
    return tornado.web.Application([
        (r"/", HelloHandler),
    ])


def main():

    global SHORT_TIMER

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', action='store_true', dest='test')
    args = parser.parse_args()  

    print(args.test)

    if args.test:
         SHORT_TIMER = True
         print("Short timer mode. For test.")

    setupGpio()
    setupValues()
    return 0



if __name__== "__main__":
    main()
    app = make_app()
    app.listen(SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()

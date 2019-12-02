import RPi.GPIO as GPIO
import time
import socket
import threading
#declaracion de pines
pinML=(19,15,26)# RBPi
pinMR=(21,23,24)# RBPi
pinServos=(7,13)
#limpiamos los puertos
#declaracion de entradas y salidas
GPIO.setmode(GPIO.BOARD)#RBPi
GPIO.setup(pinML[0],GPIO.OUT)
GPIO.setup(pinML[1],GPIO.OUT)
GPIO.setup(pinMR[0],GPIO.OUT)
GPIO.setup(pinMR[1],GPIO.OUT)
#creacion de pines PWM
GPIO.setup(pinML[2],GPIO.OUT)#RBPi
GPIO.setup(pinMR[2],GPIO.OUT)#RBPi
pwmL=GPIO.PWM(pinML[2],50)#pin,freq #RBPi
pwmR=GPIO.PWM(pinMR[2],50)#pin,freq #RBPi
pwmL.start(0)#CT  #RBPi
pwmR.start(0)#CT  #RBPi
#creacion de senales de servo
#GPIO.setup(pinServos[0],GPIO.OUT)#RBPi
#GPIO.setup(pinServos[1],GPIO.OUT)#RBPi
#servo1=GPIO.PWM(pinServos[0],50)#pin,freq #RBPi
#servo2=GPIO.PWM(pinServos[1],50)#pin,freq #RBPi
#servo1.start(6)#CT  #RBPi
#servo2.start(7)#CT  #RBPi
#time.sleep(10)
def servos(p1,p2):
    s1=p1/18+2.5
    s2=p2/18+2.5
    servo1.ChangeDutyCycle(s1) #RBPi
    servo2.ChangeDutyCycle(s2) #RBPi

#metodos
def motores(sl,sr):
    #inicio de los PWM con un CT
    pwmL.ChangeDutyCycle(abs(sl)) #RBPi
    pwmR.ChangeDutyCycle(abs(sr)) #RBPi
    #sentidos de giro
    if sl>0:
        GPIO.output(pinML[0],True) #RBPi
        GPIO.output(pinML[1],False) #RBPi
    else:
        GPIO.output(pinML[0],False) #RBPi
        GPIO.output(pinML[1],True) #RBPi

    if sr>0:
        GPIO.output(pinMR[0],True) #RBPi
        GPIO.output(pinMR[1],False) #RBPi
    else:
        GPIO.output(pinMR[0],False) #RBPi
        GPIO.output(pinMR[1],True) #RBPi

class Remote(threading.Thread):
    def __init__(self,udpIP,udpPort):
        threading.Thread.__init__(self)
        self.udpIP=udpIP
        self.udpPort=udpPort
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind((self.udpIP,self.udpPort))
        self.isRunning=True
        self.motores=[0,0]
    def run(self):
        while self.isRunning:
            data,addr=self.sock.recvfrom(1024)
            temp=data.split(":")
            if len(temp)==3:
                if temp[0]=="Robot" and temp[1]=="robot123":
                    temp=temp[2].split(",")
                    if temp[0]=="apagar":
                        self.isRunning=False
                    elif temp[0]=="motores":
                        self.motores[0]=int(temp[1])
                        self.motores[1]=int(temp[2])

        #
remoto=Remote("192.168.1.15",5005)
remoto.start()
i=0
while remoto.isRunning:
    i+=1
    motores(remoto.motores[0],remoto.motores[1])
    time.sleep(1)
    print i,remoto.motores
#detenemos los pines PWM
pwmL.stop() #RBPi
pwmR.stop() #RBPi
#limpiamos los puerto
GPIO.cleanup() #BBB y RBPi
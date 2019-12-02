import serial
import time
import threading
import random
import socket

UDP_IP="192.168.0.102"
UDP_PORT=5005

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

class RobotBase(threading.Thread):
	def __init__(self,real):
		threading.Thread.__init__(self)
		print "Robot iniciado"
		self.real=real
		self.dataOut=[0,128,128,90,90,0,0,0,0,0]
		self.dataIn=[0,0,0,0,0,0,0,0,0,0]
		self.runBase=True
		self.mot=[0,0]
		self.serv=[90,90]
	def SetSerial(self,port,baud):
		if self.real:
			self.ser=serial.Serial(port,baud,timeout=0.5)
	def ComBase(self):
		if self.real:
			self.dataOut[1]=self.mot[0]+128
			self.dataOut[2]=self.mot[1]+128
			if self.serv[0]>105:
				 self.dataOut[3]=105
			elif self.serv[0]<30:
                                 self.dataOut[3]=30
			else:
				self.dataOut[3]=self.serv[0]
			self.dataOut[4]=self.serv[1]
			if self.dataOut[0]==1:
				self.dataOut[0]=0
			else:
				self.dataOut[0]=1
			out="#O"
			crc=0
			for e in self.dataOut:
				out+=chr(e)
				crc+=e
			while crc>255:
				crc-=256
			out+=chr(crc)
			self.ser.write(out)
			self.ser.flush()#vaciar buffer del puerto serie
			time.sleep(0.01)
			buff=self.ser.readline()
			cad=buff.split(":")
			if cad[0]=="Robot" and len(cad)==2:
				c=cad[1].split(" ")
				i=0
				for e in c:
					self.dataIn[i]=float(e)
					i+=1

	def run(self):
		while self.runBase:
			self.ComBase()
			time.sleep(0.01)

base=RobotBase(True)
base.SetSerial('/dev/ttyO4',115200)
#base.SetSerial('/dev/ttyAMA0',115200)#RBPi
base.start()
j=0
i=0
while base.runBase:
	data,addr=sock.recvfrom(1024)#35000
	d=data.split(":")
	if d[0]=="Robot" and d[1]=="robot123":
		d1=d[2].split(" ")
		if len(d1)==1:
			if d1[0]=="adelante":
				base.mot=[40,40]
			elif d1[0]=="atras":
				base.mot=[-40,-40]
			elif d1[0]=="derecha":
				base.mot=[40,-40]
			elif d1[0]=="izquierda":
				base.mot=[-40,40]
			elif d1[0]=="salir":
				base.runBase=False
			elif d1[0]=="detener":
				base.mot=[0,0]
		if len(d1)==2:
			if d1[0]=="pan":
				base.serv[1]=int(d1[1])
			if d1[0]=="tilt":
                base.serv[0]=int(d1[1])
	
	print "Salida:",base.dataOut,"Entrada:",base.dataIn


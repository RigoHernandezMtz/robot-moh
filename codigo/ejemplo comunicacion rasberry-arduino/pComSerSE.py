import serial
import time
import threading
import random

class RobotBase(threading.Thread):
	def __init__(self,real):
		threading.Thread.__init__(self)
		print "Robot iniciado"
		self.real=real
		self.dataOut=[0,128,128,90,90,0,0,0,0,0]
		self.dataIn=[0,0,0,0,0,0,0,0,0,0]
		self.runBase=True
	def SetSerial(self,port,baud):
		if self.real:
			self.ser=serial.Serial(port,baud,timeout=0.5)
	def ComBase(self):
		if self.real:
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
			cad=buff.split(" ")
			if cad[0]=="Robot:" and len(cad)==11:
				i=0
				for e in cad[1:]:
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

i=0
while i<30:
	i+=1
	#j=1
	#while j<10:
	#	base.dataOut[j]=random.randint(0,255)
	#	j+=1
	print "Salida:",base.dataOut,"Entrada:",base.dataIn
	time.sleep(1)
base.runBase=False
import serial
import time
import threading
import random
import socket

UDP_IPRecv="192.168.0.122"
UDP_PORTRecv=5005

UDP_IP="192.168.0.100"
UDP_PORT=5005

#sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.bind((UDP_IP,UDP_PORT))

class Remote(threading.Thread):
	def __init__(self):
		print "Control remoto creado"
		threading.Thread.__init__(self)
		self.udpIP="127.0.0.1"
		self.udpPort=15555
		self.udpIPRecv="127.0.0.1"
		self.udpPortRecv=15666
		self.instruction="None"
		self.messFromJoy="None"
		self.thereMess=False
		self.isRunning=True
	def SetSocketToSend(self,ip,port):
		self.udpIP=ip
		self.udpPort=port
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	def SetSocketToRecv(self,ip,port):
		self.udpIPRecv=ip
		self.udpPortRecv=port
		self.sockRecv=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	def SendInfo(self,cad):
		stringOut="robot:"+cad
		self.sock.sendto(stringOut,(self.udpIP,self.udpPort))
	
	def run(self):
		self.sockRecv.bind((self.udpIPRecv,self.udpPortRecv))
		print "leyendo datos del remoto"
		while self.isRunning:
			data,addr=self.sockRecv.recvfrom(1024)
			temp=data.split(":")
			if len(temp)==4:
				if temp[0]=="Robot" and temp[1]=="robot123":
					if temp[2]=="EndProgram":
						self.isRunning=False
						self.instruction="EndProgram"
					if temp[2]=="JoyStick":
						self.messFromJoy=temp[3]
						self.thereMess=True


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
		self.encD= 0.0
		self.encI= 0.0
		self.sonar=0.0
		self.volt= 0.0

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
				if len(c)==5:
					self.encD= float(c[0])
					self.encI= float(c[1])
					self.sonar=float(c[2])
					self.volt= float(c[3])

	def run(self):
		while self.runBase:
			self.ComBase()
			time.sleep(0.01)
	
	def Remote(self,mess,th):
		if th==True:
			cad=mess.split("_")
			if len(cad)==2:
				if cad[0]=="motores":
					m=cad[1].split(" ")
					if len(m)==2:
						self.mot[0]=int(m[0])
						self.mot[1]=int(m[1])
				if cad[0]=="pan":
					self.serv[1]=int(cad[1])
				if cad[0]=="tilt":
					self.serv[0]=int(cad[1])



base=RobotBase(True)
base.SetSerial('/dev/ttyO4',115200)
base.start()

remoto=Remote()
remoto.SetSocketToSend(UDP_IP,UDP_PORT)#IP Remoto
remoto.SetSocketToRecv(UDP_IPRecv,UDP_PORTRecv)#IP Robot
remoto.start()

j=0
i=0
while base.runBase:
	base.Remote(remoto.messFromJoy,remoto.thereMess)
	time.sleep(0.1)
	print "c:",i,"Salida:",base.dataOut,"Entrada:",base.dataIn
	infoS=str(base.encI)+" "+str(base.encD)+" "
	infoS+=str(base.sonar)+" "+str(base.volt)
	if i%10==0:
		remoto.SendInfo(infoS)
	base.runBase=remoto.isRunning
	i+=1

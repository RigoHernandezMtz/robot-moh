import pygame
import time
import socket
# direccion IP y numero de puerto para envio
UDP_IP="127.0.0.1"
UDP_PORT=5005

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
i=0

#iniciar el modulo de pygame
pygame.init()
#iniciar el uso de joystick
pygame.joystick.init()
#buscar joysticks conectados
joyCount=pygame.joystick.get_count()

if joyCount>0:
	joystick=pygame.joystick.Joystick(0)
	joystick.init()#inicia el js0
	name=joystick.get_name()
	axes=joystick.get_numaxes()
	buttons=joystick.get_numbuttons()
	hats=joystick.get_numhats()
	print "Nombre:",name,"Ejes:",axes,"Botones:",buttons,"Hats:",hats

axis=[0.0,0.0,0.0,0.0,0.0,0.0]
button=[0,0,0,0,0,0,0,0,0,0,0]

while not button[6]:
	pygame.event.get()

	for i in range(axes):# leer los 6 ejes
		axis[i]=joystick.get_axis(i)

	for i in range(buttons):
		button[i]=joystick.get_button(i)

	#Datos para motores
	sR=int( (-axis[1]-axis[0])*100 )
	sL=int( (-axis[1]+axis[0])*100 )
	if sR<-100: sR=-100
	if sR>100:  sR=100
	if sL<-100: sL=-100
	if sL>100:  sL=100
	#envio de datos a la RBPi o BBB
	out="Robot:robot123:"+str(sL)+" "+str(sR)
	sock.sendto(out,(UDP_IP,UDP_PORT))
	print "vI:",sL,"vD:",sR
	#print "Hat:",hat,"Botones:",button,"axes:",axis
	time.sleep(0.1)

pygame.quit()
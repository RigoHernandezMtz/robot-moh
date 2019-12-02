char dataIn[13];
int i=0;
void setup(){
	Serial.begin(115200);
	pinMode(13,OUTPUT);
}

void loop(){
	remoto();
}

void remoto(){
	char temp;
	if(Serial.available()>12){
		temp=Serial.read();
		if(temp=='#'){
			temp=Serial.read();
			if(temp=='O'){
				i=0;
				while(i<11){
					dataIn[i]=Serial.read();
					i+=1;
				}//fin while 11
				char crc=0;
				for(i=0;i<10;i++)
					crc+=dataIn[i];
				if(crc==dataIn[10]){
					//acondicionamiento de variables
					digitalWrite(13,dataIn[0]);
					//fin acodicionamiento
				}//fin crc
				Serial.print("Robot: ");
				Serial.print(random(0,10));
				Serial.print(" ");
				Serial.print(random(10,20));
				Serial.print(" ");
				Serial.print(random(20,30));
				Serial.print(" ");
				Serial.print(random(30,40));
				Serial.print(" ");
				Serial.print(random(40,50));
				Serial.print(" ");
				Serial.print(random(50,60));
				Serial.print(" ");
				Serial.print(random(60,70));
				Serial.print(" ");
				Serial.print(random(70,80));
				Serial.print(" ");
				Serial.print(random(80,90));
				Serial.print(" ");
				Serial.println(random(90,100));
			}//fin O

		}//fin #

	}//fin lectura 12
} // fin remoto()

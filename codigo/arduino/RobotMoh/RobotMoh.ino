#include <Servo.h>
#define ECHO_PIN A4
#define TRIGER_PIN A5
#define S1_PIN  4
#define S2_PIN  5
#define ENCD_A    0  //Digital PIN 2
#define ENCD_B    A0  //Digital PIN 22
#define ENCI_A    1  //Digital PIN 3
#define ENCI_B    A1  //Digital PIN 23
#define VOLT_PIN  A3
#define MOTD_A  7
#define MOTD_B  8
#define MOTD_P  6

#define MOTI_A  9
#define MOTI_B  10
#define MOTI_P  11

#define LED 13

int time=0;

Servo s1;
Servo s2;
long encD=0,encI=0;
long t0=millis();
long t0Rem=millis();
long vDer=0,vIzq=0;
long s[2]={90,90};
float volt;
void setup(){
  pinMode(ECHO_PIN,INPUT);
  pinMode(TRIGER_PIN,OUTPUT);
  pinMode(LED,OUTPUT);
  Serial.begin(115200);
  s1.attach(S1_PIN);
  s2.attach(S2_PIN);
  s1.write(90);
  s2.write(80);
  attachInterrupt(ENCD_A,inte0,RISING);
  attachInterrupt(ENCI_A,inte1,RISING);
  pinMode(MOTD_A,OUTPUT);
  pinMode(MOTD_B,OUTPUT);
  pinMode(MOTI_A,OUTPUT);
  pinMode(MOTI_B,OUTPUT);
}

void loop(){
  s1.write(s[0]);
  s2.write(s[1]);
  
  if((millis()-t0)>200){
    time=leer_sonar()/10;
    t0=millis();
  }
  if((millis()-t0Rem)>500)
    motores(0,0);
    

  volt=analogRead(VOLT_PIN);
  volt=volt*9.05/1024;
  remoto();
}

long leer_sonar(){
   long tempo=0;
   digitalWrite(TRIGER_PIN,HIGH);
   delayMicroseconds(11);
   digitalWrite(TRIGER_PIN,LOW);
   int err=0;   
   while(!digitalRead(ECHO_PIN) && err<4000){
     err+=1; 
   }
   if(err<4000){
      while(digitalRead(ECHO_PIN) && tempo<1000)
         tempo=tempo+1;   
   }
   else
      tempo=9999;
   return tempo;
}




void inte0(){
  if(digitalRead(ENCD_B)){
    encD=encD-1;
  }
  else{
    encD=encD+1;
  }
}
void inte1(){
  if(!digitalRead(ENCI_B)){
    encI=encI+1;
  }
  else{
    encI=encI-1;
  }
}

void motores(float vi, float vd){
  if(vi>0){
    digitalWrite(MOTI_A,HIGH);
    digitalWrite(MOTI_B,LOW);
  }
  else{
    digitalWrite(MOTI_A,LOW);
    digitalWrite(MOTI_B,HIGH);
  }
  if(vd>0){
    digitalWrite(MOTD_A,HIGH);
    digitalWrite(MOTD_B,LOW);
  }
  else{
    digitalWrite(MOTD_A,LOW);
    digitalWrite(MOTD_B,HIGH);
  }
  analogWrite(MOTI_P,abs(vi*2.55));
  analogWrite(MOTD_P,abs(vd*2.55));
}

void remoto(){
  char temp;
  char dataIn[13];
  int i=0;
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
          digitalWrite(LED,dataIn[0]);
          
          vIzq=byte(dataIn[1]);
          vIzq-=128;
          if(vIzq<-100)
            vIzq=-100;
          if(vIzq>100)
            vIzq=100;
            
          vDer=byte(dataIn[2]);
          vDer-=128;
          if(vDer<-100)
            vDer=-100;
          if(vDer>100)
            vDer=100;
            
          s[0]=byte(dataIn[3]);
          if(s[0]>180)
            s[0]=180;
          s[1]=byte(dataIn[4]);
          if(s[1]>180)
            s[1]=180;
          
          //fin acodicionamiento
          //envio de datos
          Serial.print("Robot:");
          Serial.print(encD);
          Serial.print(" ");
          Serial.print(encI);
          Serial.print(" ");
          Serial.print(time);
          Serial.print(" ");
          Serial.print(volt);
          Serial.print(" ");
          Serial.println(101);
          //fin de envio de datos
          motores(vIzq,vDer);
          t0Rem=millis();
        }//fin crc
        
      }//fin O

    }//fin #

  }//fin lectura 12
} // fin remoto()

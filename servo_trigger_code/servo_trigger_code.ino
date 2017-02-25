#include<Servo.h>
int odo[20]={2,0,4,0,6,0,7,0,8,0,9,0,10,0,12,0,13,0,14,0};
int a=1;
int stopcount = 0;
Servo ser;
int pos = 0;
void setup() {
  ser.attach(9);
  pinMode(2,INPUT);
Serial.begin(9600); // set the baud rate
// print "Ready" once
}
void loop() {
char inByte = ' ';
 // only send data back if data has been sent
 if(Serial.available()){
inByte = Serial.read(); // read the incoming data
if(inByte == 'T')
{
  //Perform servo rotation
   for (int i=0;i<180;i++)
     {ser.write(i);delay(10);}  
     ser.write(0);
    
   
    //Serial.println('D');
}
 }

 
//Serial.println(digitalRead(2));
if(!digitalRead(2))
{
  
 a++; 
Serial.println('K'); 
Serial.println(odo[stopcount]);
stopcount++;
delay(1000);
}

else {a++;}

//Serial.println('Q');
delay(100); // delay for 1/10 of a second
}

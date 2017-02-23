#include<Servo.h>

Servo ser;
int pos = 0;
void setup() {
  ser.attach(9);
Serial.begin(9600); // set the baud rate
Serial.println("Ready"); // print "Ready" once
}
void loop() {
char inByte = ' ';
if(Serial.available()){ // only send data back if data has been sent
char inByte = Serial.read(); // read the incoming data
if(inByte == 'T')
{
  //Perform servo rotation
   for (int i=0;i<180;i++)
     {ser.write(i);delay(10);}  
     ser.write(0);
}
}
delay(100); // delay for 1/10 of a second
}

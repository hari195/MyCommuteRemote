#include<Servo.h>
int odo[5]={1,3,4,2,1};
int a;
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
//char inByte = Serial.read(); // read the incoming data
if(inByte == 'T')
{
  //Perform servo rotation
   for (int i=0;i<180;i++)
     {ser.write(i);delay(10);}  
     ser.write(0);
     Serial.println('D');
}

//Serial.println(digitalRead(2));
if(!digitalRead(2))
{
  
Serial.println('K'); 
Serial.println(odo[stopcount%5]);
stopcount++;
delay(1000);
}

Serial.println('Q');
delay(100); // delay for 1/10 of a second
}

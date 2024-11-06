// Include the Servo library 
#include <Servo.h> 
// Declare the Servo pin 
int servoPin = 3; 
// Create a servo object 
Servo Servo1; 
int pos = 0;    // variable to store the servo position

long randNumber_temp;
long randNumber_dew;
long randNumber_humidity;
long randNumber_dust;

int ledPin = 13; // Pin where LED is connected

void setup() {
  // We need to attach the servo to the used pin number 
  Servo1.attach(servoPin); 
  Servo1.write(pos); 

  pinMode(ledPin, OUTPUT); 
  
  Serial.begin(9600);
  
  randomSeed(analogRead(0));
  
  Serial.println("Sending values: ");
}

void loop() {
  // print a random number from 17 to 40
  randNumber_temp = random(17, 40);
  // print a random number from 0 to 30
  randNumber_dew = random(30.0);
  // print a random number from 13 to 100
  randNumber_humidity = random(13, 100);
  // print a random number from 100 to 700
  randNumber_dust = random(100, 700);
  
  Serial.print(randNumber_temp);
  Serial.print(" | ");
  Serial.print(randNumber_dew);
  Serial.print(" | ");
  Serial.println(randNumber_humidity);
  
  // read command
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      digitalWrite(ledPin, HIGH); // Turn LED on
      for (pos = 0; pos <= 5; pos += 1){
        // Make servo go to 0 degrees 
        Servo1.write(0); 
        delay(10); 
        // Make servo go to 90 degrees 
        Servo1.write(90); 
        delay(10); 
        // Make servo go to 180 degrees 
        Servo1.write(180); 
        delay(10);
        // Make servo go to 90 degrees 
        Servo1.write(90); 
        delay(10); 
        // Make servo go to 0 degrees 
        Servo1.write(0); 
        delay(10); 
      } 
    } else if (command == '0') {
      digitalWrite(ledPin, LOW); // Turn LED off
      Servo1.write(0); 
      delay(10); 
    }
  }

  delay(1000*5);


}

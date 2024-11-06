#include <Servo.h> 
// Declare the Servo pin 
int servoPin = 3; 
// Create a servo object 
Servo Servo1; 
int pos = 0;    // variable to store the servo position

// constants won't change. They're used here to set pin numbers:
const int buttonPin = 4;  // the number of the pushbutton pin
const int ledPin = 13;    // the number of the LED pin

// variables will change:
int buttonState = 0;  // variable for reading the pushbutton status

void setup() {
  Servo1.attach(servoPin); 
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
}

void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  // if (buttonState == HIGH) 
  if (buttonState == LOW) 
  {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    // digitalWrite(ledPin, LOW);
    // Servo1.write(18); 
    // delay(100);
    // Servo1.write(0); 
    // delay(100); 
    for (pos = 0; pos <= 90; pos += 5)
    {
    // Make servo go to 0 degrees 
        Servo1.write(pos); 
        delay(500); 
    }
  } 
  else 
  {
    // turn LED off:
    digitalWrite(ledPin, LOW);
    // Make servo go to 0 degrees 
    Servo1.write(0); 
    delay(100); 
    
  }
}

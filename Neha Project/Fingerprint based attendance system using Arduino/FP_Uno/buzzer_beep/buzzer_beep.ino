int buzzerPin = 13; // LED connected to digital pin 13

void setup() {
  pinMode(buzzerPin, OUTPUT); // set the digital pin as output
}

void loop() {
  beep();
}

void beep() {
  digitalWrite(buzzerPin, HIGH); // turn the LED on
  delay(1000); // wait for 1 second
  digitalWrite(buzzerPin, LOW); // turn the LED off
  delay(1000); // wait for 1 second  
}
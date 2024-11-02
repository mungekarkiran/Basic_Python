long randNumber_temp;
long randNumber_dew;
long randNumber_humidity;

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));
  Serial.println("Sending values: ");
}

void loop() {
  // print a random number from 17 to 40
  randNumber_temp = random(17, 40);
  // Serial.print("temp: ");
  Serial.print(randNumber_temp);

  // print a random number from 0 to 30
  randNumber_dew = random(30.0);
  // Serial.print(" | dew: ");
  Serial.print(" | ");
  Serial.print(randNumber_dew);

  // print a random number from 13 to 100
  randNumber_humidity = random(13, 100);
  // Serial.print(" | humidity: ");
  Serial.print(" | ");
  Serial.println(randNumber_humidity);
  // Serial.println("----");
  // Serial.print(randNumber_temp);
  // Serial.print(" | ");
  // Serial.print(randNumber_dew);
  // Serial.print(" | ");
  // Serial.print(randNumber_humidity);
  // Serial.println(" ");

  delay(1000);
}

//Air Quality - MQ-135 Sensor Test
void setup() {
  // note down the acceptable CO2 ppm values:
  // 400 ppm – 750 ppm: Good for health
  // 750 ppm – 1200 ppm: Take care
  // 1200 ppm (and above): Harmful to health
  
  // put your setup code here, to run once:
  pinMode(A0, INPUT);
  Serial.begin(9600);
}

void loop() {
  
  // put your main code here, to run repeatedly:
  int mq_value = analogRead(A0);
  Serial.print("MQ-135 Sensor CO2 Value : ");
  Serial.print(mq_value, DEC);
  Serial.print(" PPM");
  int mq_value_in_pct = map(mq_value, 0, 850, 0, 100);
  Serial.print(" || in % : ");
  Serial.print(mq_value_in_pct, DEC);
  Serial.println("% in Air.");
   
  delay(1000); // 1000 == 1 sec.
}

#define RAIN_ANALOG_PIN A0    // Analog pin connected to A0 on the raindrop sensor
#define RAIN_DIGITAL_PIN 7    // Digital pin connected to D0 on the raindrop sensor

void setup() {
  // Start the serial communication
  Serial.begin(9600);

  // Set the digital pin for rain detection as input
  pinMode(RAIN_DIGITAL_PIN, INPUT);
}

void loop() {
  // Read the analog value (rain intensity)
  int rainIntensity = analogRead(RAIN_ANALOG_PIN);

  // Read the digital value (rain presence)
  int rainPresence = digitalRead(RAIN_DIGITAL_PIN);

  // Print the analog value (rain intensity) to the Serial Monitor
  Serial.print("Rain Intensity (Analog): ");
  Serial.println((30-rainIntensity/30)+10);  // Range from 0 to 1023

  // Check the rain presence via digital output
  if (rainPresence == LOW) {
    Serial.println("Rain Detected (Digital: LOW)");
  } else {
    Serial.println("No Rain (Digital: HIGH)");
  }

  // Wait for 1 second before taking another reading
  delay(5000);
}

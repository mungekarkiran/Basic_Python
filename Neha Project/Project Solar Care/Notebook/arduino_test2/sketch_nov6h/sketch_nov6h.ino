// Define pin for dust sensor
#define DUST_SENSOR_PIN A2

// Function to get an accurate reading from the dust sensor
float getDustDensity() {
  // Take multiple readings and average them to get a stable value
  const int numSamples = 10; // Number of samples to average
  int totalValue = 0;
  
  for (int i = 0; i < numSamples; i++) {
    int reading = analogRead(DUST_SENSOR_PIN);
    totalValue += reading;
    delay(50); // Short delay between samples
  }

  // Calculate the average value
  int averageValue = totalValue / numSamples;

  // Convert the analog value to voltage
  float voltage = averageValue * (5.0 / 1023.0); // Convert ADC reading to voltage

  // Debug: Print the raw analog value and voltage for verification
  Serial.print("Average Analog Value: ");
  Serial.println(averageValue);
  Serial.print("Calculated Voltage (V): ");
  Serial.println(voltage, 3); // Print voltage with 3 decimal places

  // Convert voltage to dust density using an adjusted formula
  float dustDensity = (voltage - 0.5) * 1000; // Adjust baseline voltage as needed

  // Ensure the value is non-negative
  if (dustDensity < 0) {
    dustDensity = 0;
  }

  return dustDensity;
}

void setup() {
  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  // Get and print the dust density reading
  float dustDensity = getDustDensity();
  Serial.print("Dust Density (µg/m³): ");
  Serial.println(dustDensity);

  // Wait for a short time before the next reading
  delay(5000); // Adjust as necessary
}

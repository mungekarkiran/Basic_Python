#include <DHT.h>

// DHT Sensor setup
#define DHTPIN 4        // Pin connected to the DHT sensor
#define DHTTYPE DHT11   // Define the type of DHT sensor (DHT11)

DHT dht(DHTPIN, DHTTYPE);  // Initialize the DHT sensor

// Rain Sensor setup
#define RAIN_ANALOG_PIN A0    // Analog pin connected to A0 on the raindrop sensor
#define RAIN_DIGITAL_PIN 7    // Digital pin connected to D0 on the raindrop sensor

void setup() {
  // Start the serial communication
  Serial.begin(9600);

  // Initialize the DHT sensor
  dht.begin();

  // Set the digital pin for rain detection as input
  pinMode(RAIN_DIGITAL_PIN, INPUT);
}

void loop() {
  // Read temperature and humidity from the DHT sensor
  float temperature = dht.readTemperature(); // Temperature in Celsius
  float humidity = dht.readHumidity();       // Humidity in percentage

  // Check if the readings are valid
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    // Print the temperature and humidity to the Serial Monitor
    Serial.print("Temperature: ");
    Serial.print(temperature - 5);  // Adjusting temperature as per your requirement
    Serial.println(" °C");

    Serial.print("Humidity: ");
    Serial.print(humidity + 30);  // Adjusting humidity as per your requirement
    Serial.println(" %");
  }

  // Read the analog value (rain intensity) from the rain sensor
  int rainIntensity = analogRead(RAIN_ANALOG_PIN);

  // Read the digital value (rain presence) from the rain sensor
  int rainPresence = digitalRead(RAIN_DIGITAL_PIN);

  // Print the analog value (rain intensity) to the Serial Monitor
  Serial.print("Rain Intensity (Analog): ");
  Serial.println((30 - rainIntensity / 30) + 10);  // Adjusting rain intensity

  // Check the rain presence via the digital sensor
  if (rainPresence == LOW) {
    Serial.println("Rain Detected (Digital: LOW)");
  } else {
    Serial.println("No Rain (Digital: HIGH)");
  }

  // Wait for a short time before taking another reading
  delay(5000); // Delay of 5 seconds before repeating the loop
}

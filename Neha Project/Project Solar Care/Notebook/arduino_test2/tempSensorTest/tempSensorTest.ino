#include <DHT.h>

// DHT Sensor setup
#define DHTPIN 4    // Pin connected to the DHT sensor
#define DHTTYPE DHT11 // Define the type of DHT sensor (DHT11)

DHT dht(DHTPIN, DHTTYPE); // Initialize the DHT sensor

void setup() {
  // Start the serial communication
  Serial.begin(9600);

  // Initialize the DHT sensor
  dht.begin();
}

void loop() {
  // Read temperature and humidity from the DHT sensor
  float temperature = dht.readTemperature(); // Temperature in Celsius
  float humidity = dht.readHumidity(); // Humidity in percentage

  // Check if the readings are valid
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print the temperature and humidity to the Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperature-5);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity+30);
  Serial.println(" %");

  // Wait for 2 seconds before taking another reading
  delay(10000);
}

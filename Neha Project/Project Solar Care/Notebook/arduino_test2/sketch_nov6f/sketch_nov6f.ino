#include <DHT.h>

// DHT Sensor setup
#define DHTPIN 4        // Pin connected to the DHT sensor
#define DHTTYPE DHT11   // Define the type of DHT sensor (DHT11)

DHT dht(DHTPIN, DHTTYPE);  // Initialize the DHT sensor

// Rain Sensor setup
#define RAIN_ANALOG_PIN A0    // Analog pin connected to A0 on the raindrop sensor
#define RAIN_DIGITAL_PIN 7    // Digital pin connected to D0 on the raindrop sensor

// Light sensor setup
#define LIGHT_SENSOR_PIN A1   // Analog pin connected to the light sensor (LDR)
#define LIGHT_THRESHOLD 200   // Threshold value to detect daylight (adjusted threshold)

#define TEMP_THRESHOLD 30     // Temperature threshold for cleaning
#define DEW_THRESHOLD 25      // Dew threshold for cleaning
#define HUMIDITY_THRESHOLD 80 // Humidity threshold for cleaning

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
    Serial.print(temperature);
    Serial.println(" °C");

    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  }

  // Read the analog value (rain intensity) from the rain sensor
  int rainIntensity = analogRead(RAIN_ANALOG_PIN);

  // Read the digital value (rain presence) from the rain sensor
  int rainPresence = digitalRead(RAIN_DIGITAL_PIN);

  // Print the analog value (rain intensity) to the Serial Monitor
  Serial.print("Rain Intensity (Analog): ");
  Serial.println(rainIntensity);

  // Check the rain presence via the digital sensor
  if (rainPresence == LOW) {
    Serial.println("Rain Detected (Digital: LOW)");
  } else {
    Serial.println("No Rain (Digital: HIGH)");
  }

  // Read light sensor value to determine day or night
  int lightLevel = analogRead(LIGHT_SENSOR_PIN);

  // Print the light sensor reading (for debugging)
  Serial.print("Light Level: ");
  Serial.println(lightLevel);

  // Check if it is daytime (based on light level)
  bool isDaytime = (lightLevel > LIGHT_THRESHOLD); // Light above threshold = Daytime, else Nighttime

  // Print whether it's day or night
  if (isDaytime) {
    Serial.println("Daytime (Sunlight Detected)");
  } else {
    Serial.println("Nighttime (No Sunlight Detected)");
  }

  // Decide whether cleaning should be initiated based on sunlight detection
  bool cleaningRequired = false;

  if (isDaytime) {  // Cleaning is initiated when it's daytime (sunlight detected)
    Serial.println("Sunlight detected, cleaning initiated.");
    cleaningRequired = true;
  } else {
    cleaningRequired = false;
  }

  // Print the decision for cleaning
  if (cleaningRequired) {
    Serial.println("Cleaning initiated.");
    // Code to activate cleaning mechanism (e.g., servo motor)
  } else {
    Serial.println("No cleaning required.");
  }

  // Wait for a short time before taking another reading
  delay(5000); // Delay of 5 seconds before repeating the loop
}

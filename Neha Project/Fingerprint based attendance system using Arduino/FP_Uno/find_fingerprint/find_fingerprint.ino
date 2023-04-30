#include <Adafruit_Fingerprint.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F, 16, 2); // set the LCD address to 0x27 for a 16 chars and 2 line display

#if (defined(__AVR__) || defined(ESP8266)) && !defined(__AVR_ATmega2560__)
SoftwareSerial mySerial(2, 3);
#else
#define mySerial Serial1
#endif

int buzzerPin = 13;
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

void setup()
{
  lcd.init();         // initialize the lcd
  lcd.backlight();    // Turn on the LCD screen backlight  
  
  Serial.begin(9600);
  while (!Serial);  // For Yun/Leo/Micro/Zero/...
  delay(100);
  Serial.println("\nFinger detect test");

  pinMode(buzzerPin, OUTPUT);

  // set the data rate for the sensor serial port
  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    Serial.println("Did not find fingerprint sensor :(");
    while (1) { delay(1); }
  }

  Serial.println(F("Reading sensor parameters"));
  finger.getParameters();
  Serial.print(F("Status: 0x")); Serial.println(finger.status_reg, HEX);
  Serial.print(F("Sys ID: 0x")); Serial.println(finger.system_id, HEX);
  Serial.print(F("Capacity: ")); Serial.println(finger.capacity);
  Serial.print(F("Security level: ")); Serial.println(finger.security_level);
  Serial.print(F("Device address: ")); Serial.println(finger.device_addr, HEX);
  Serial.print(F("Packet len: ")); Serial.println(finger.packet_len);
  Serial.print(F("Baud rate: ")); Serial.println(finger.baud_rate);

  finger.getTemplateCount();

  if (finger.templateCount == 0) {
    Serial.print("Sensor doesn't contain any fingerprint data. Please run the 'enroll' example.");
  }
  else {
    Serial.println("Waiting for valid finger...");
      Serial.print("Sensor contains "); Serial.print(finger.templateCount); Serial.println(" templates");
  }
}

void loop()                     // run over and over again
{
  getFingerprintID();
  delay(50);            //don't ned to run this at full speed.
}

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      // Serial.println("No finger detected");
      Serial.println(".");

      lcd.setCursor(3, 0);
      lcd.print("Welcome to ");
      lcd.setCursor(3, 1);
      lcd.print("I.T. Dept.");
      delay(2000);
      lcd.clear();
                      
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("Did not find a match");
    
    lcd.setCursor(0, 0);
    lcd.print("Match not found.");
    lcd.setCursor(0, 1);
    lcd.print("Try again!");
    
    not_found_beep();  
    lcd.clear();
             
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);

  if (finger.fingerID == 1){
  Serial.println("Hello Kiran Mungekar. \nYour attendance is marked successfully..."); Serial.println("ID # 01"); 
  
  lcd.setCursor(0, 0);
  lcd.print("Kiran Mungekar");
  lcd.setCursor(0, 1);
  lcd.print("Attendance marked");
  // delay(3000);
  
  beep();  
  delay(5000);   
} else if (finger.fingerID == 2){
  Serial.println("Hello Dinesh Parab. \nYour attendance is marked successfully..."); Serial.println("ID # 02"); 
  
  lcd.setCursor(0, 0);
  lcd.print("Dinesh Parab");
  lcd.setCursor(0, 1);
  lcd.print("Attendance marked");
  
  beep();  
  delay(5000);
} else if (finger.fingerID == 3){
  Serial.println("Hello Suneeta Nathan. \nYour attendance is marked successfully..."); Serial.println("ID # 03"); 
  
  lcd.setCursor(0, 0);
  lcd.print("Suneeta Nathan");
  lcd.setCursor(0, 1);
  lcd.print("Attendance marked");
  
  beep();
  delay(5000);
} else if (finger.fingerID == 4){
  Serial.println("Hello Sunny Bam. \nYour attendance is marked successfully..."); Serial.println("ID # 04"); 
  
  lcd.setCursor(0, 0);
  lcd.print("Sunny Bam");
  lcd.setCursor(0, 1);
  lcd.print("Attendance marked");
  
  beep();
  delay(5000);
} else if (finger.fingerID == 5){
  Serial.println("Hello Harry Ali. \nYour attendance is marked successfully..."); Serial.println("ID # 05"); 
  
  lcd.setCursor(0, 0);
  lcd.print("Harry Ali");
  lcd.setCursor(0, 1);
  lcd.print("Attendance marked");
  
  beep();
  delay(5000);
} else if (finger.fingerID == 6){
  Serial.println("Hello Neel Shah. \nYour attendance is marked successfully..."); Serial.println("ID # 06"); 
  
  lcd.setCursor(0, 0);
  lcd.print("Neel Shah");
  lcd.setCursor(0, 1);
  lcd.print("Attendance marked");
  
  beep();
  delay(5000);
} else if (finger.fingerID == 7){
  Serial.println("Hello Deepika Padukone. \nYour attendance is marked successfully..."); Serial.println("ID # 07");   
  
  lcd.setCursor(0, 0);
  lcd.print("Deepika Padukone");
  lcd.setCursor(0, 1);
  lcd.print("Attendance marked");
  
  beep();
  delay(5000);
} else {
  Serial.print("");   
}
  lcd.clear(); 
  return finger.fingerID;
}

// returns -1 if failed, otherwise returns ID #
int getFingerprintIDez() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  return finger.fingerID;
}

void beep() {
  digitalWrite(buzzerPin, HIGH); // turn the LED on
  delay(1000); // wait for 1 second
  digitalWrite(buzzerPin, LOW); // turn the LED off
  delay(1000); // wait for 1 second  
}

void not_found_beep() {
  digitalWrite(buzzerPin, HIGH); // turn the LED on
  delay(400); // wait for 1 second
  digitalWrite(buzzerPin, LOW); // turn the LED off
  delay(100); // wait for 1 second  
  digitalWrite(buzzerPin, HIGH); // turn the LED on
  delay(400); // wait for 1 second
  digitalWrite(buzzerPin, LOW); // turn the LED off
  delay(100); // wait for 1 second  
  digitalWrite(buzzerPin, HIGH); // turn the LED on
  delay(400); // wait for 1 second
  digitalWrite(buzzerPin, LOW); // turn the LED off
  delay(100); // wait for 1 second  
}
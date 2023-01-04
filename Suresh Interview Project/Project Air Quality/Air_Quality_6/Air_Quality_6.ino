//

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // put your setup code here, to run once:
  lcd.init();
//  lcd.setCursor(0,0);
  // Turn on the blacklight and print a message.
  lcd.backlight();
//  lcd.print("Hello, world!");
}

void loop() {
  // put your main code here, to run repeatedly:
  // Do nothing here...
  lcd.clear();
  
  lcd.setCursor(0,0);
  lcd.print("Hello");
  lcd.setCursor(0,1);
  lcd.print("World");
  
  delay(2000);

  lcd.clear();
  
  lcd.setCursor(5,0);
  lcd.print("Wellcome");
  lcd.setCursor(5,1);
  lcd.print("Kiran");
  
  delay(2000);
  
}

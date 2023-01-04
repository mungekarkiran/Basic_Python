//Air Quality Final Test 7
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

int buzzerPin = 2;

void setup() {
  // put your setup code here, to run once:
  lcd.init();
  lcd.backlight();
  pinMode(A0, INPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int mq_value = analogRead(A0);
  Serial.print("MQ-135 Sensor AQI Value : ");
  Serial.print(mq_value, DEC);
  Serial.print(" PPM");
  int mq_value_in_pct = map(mq_value, 0, 850, 0, 100);
  Serial.print(" (");
  Serial.print(mq_value_in_pct, DEC);
  Serial.print("%) ");
  
  float mq_value1 = round2(analogToPPM(analogRead(A0)));
  Serial.print("|| CO2 Value : ");
  Serial.print(mq_value1);
  Serial.println(" (mg/m^3) in Air.");

  lcd.clear();

  lcd.setCursor(0,0);
  lcd.print("AQI:");
  lcd.print(mq_value);
  lcd.print("PPM(");
  lcd.print(mq_value_in_pct);
  lcd.print("%)");
  lcd.setCursor(0,1);
  lcd.print("CO2:");
  lcd.print(mq_value1);
  lcd.print(" mg/m^3");
  
  digitalWrite(buzzerPin, LOW);
  if (mq_value_in_pct > 80)
  {
    digitalWrite(buzzerPin, HIGH);
  }
  
  delay(1000);
}

double analogToPPM(int aValue)
{
  float m = -0.6527;
  float b = 1.30;
  float R0 = 23.91;
  float sensor_volt;
  float RS_gas;
  float ratio;
  int sensorValue = aValue;

  sensor_volt = sensorValue*(5.0/1023.0);
  RS_gas = ((5.0*10.0)/sensor_volt)-10.0;
  ratio = RS_gas/R0;
  double ppm_log = (log10(ratio)-b)/m;
  return ppm_log;
}

float round2(float var)
{
  // 37.66666 * 100 = 3766.66
  // 3766.66 + .5 = 3767.16    for rounding off value
  // then type cast to int so value is 3767
  // then divided by 100 so the value converted into 37.67
  float value = (int)(var * 100 + .5);
  return (float)value / 100;
}



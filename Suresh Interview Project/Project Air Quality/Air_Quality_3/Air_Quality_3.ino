//Air Quality - MQ-135 Sensor Test 3
//https://pib.gov.in/newsite/printrelease.aspx?relid=110654
//https://www.youtube.com/watch?v=LsS7cS-ahDE
//https://www.youtube.com/watch?v=ERQKDBp9FJY
//https://www.youtube.com/watch?v=FjZBt6eU9b4
//https://www.youtube.com/watch?v=b968xQr8Kwg
//https://www.youtube.com/watch?v=pgOvNURUoT0&t=131s
void setup() {
  // put your setup code here, to run once:
  pinMode(A0, INPUT);
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

  delay(2000);
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



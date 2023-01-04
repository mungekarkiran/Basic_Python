//Air Quality - MQ-135 Sensor Test 2 with MQ135.h lib.
//https://www.youtube.com/watch?v=mivNAaOEdzM
#include "MQ135.h"
#define SENSOR A0

void setup()
{
  Serial.begin(9600);
} 

void loop()
{
    MQ135 gasSensor = MQ135(SENSOR);
    float air_quality = gasSensor.getPPM();
    Serial.print("Air Quality: ");  
    Serial.print(air_quality);
    Serial.println(" PPM.");   

    delay(1000);
}

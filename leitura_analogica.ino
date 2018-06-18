
int analogPin = A0;     // potentiometer wiper (middle terminal) connected to analog pin 
                       // outside leads to ground and +5V
int val = 0;           // variable to store the value read

float scaledX;
int scale = 3;

void setup()
{
  Serial.begin(115200);   //  setup serial
  //analogReference(EXTERNAL);
  
}

float mapf(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
void loop()
{
  
  val = analogRead(analogPin);     // read the input pin
  scaledX = mapf(val, 0, 675, -scale, scale);
  Serial.print( millis());
  Serial.print(",");
  //Serial.print(val);
   //Serial.print(",");
  Serial.print(scaledX * 1000 - 680);// return mg values
 Serial.println();
 //delay(2);
}

#include <SoftwareSerial.h>
#include <Wire.h>

#define MCP4725_ADDR 0x60   

SoftwareSerial mySerial(3, 4);
int i = 0;
int compteur = 0;

void DAC_control(int value){
  Wire.beginTransmission(MCP4725_ADDR);
  Wire.write(64);                     // cmd to update the DAC
  Wire.write(value >> 4);        // the 8 most significant bits...
  Wire.write((value & 15) << 4); // the 4 least significant bits...
  Wire.endTransmission();
}

void setup() {
  Serial.begin(57600);
  Wire.begin();
  DAC_control(0);
  
  Serial.println(F("How many rounds"));
  while(!Serial.available()){
    delay(100);
  }
  if (Serial.available()){
    i = Serial.parseInt();
    Serial.read();
    Serial.println(i);
  }
  delay(1000);
  
  mySerial.begin(57600);
  DAC_control(4095);
}

void loop() {
  if (mySerial.available()){
    char inByte = mySerial.read();
    if(inByte!='X'){
      Serial.write(inByte);
    }
    else{
      char inByte = mySerial.read();
      if(inByte=='X'){
        DAC_control(0);

        if(++compteur == i){
          for (;;);
        }
        delay(4000);
        DAC_control(4095);
      }
    }
  }
}

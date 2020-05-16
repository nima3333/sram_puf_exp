#include <SoftwareSerial.h>
#include <Wire.h>

#define MCP4725_ADDR 0x60   

SoftwareSerial mySerial(3, 4);
int i = 0;
int compteur = 0;

void DAC_control(int value){
  Wire.beginTransmission(MCP4725_ADDR);
  Wire.write(64);
  Wire.write(value >> 4);
  Wire.write((value & 15) << 4);
  Wire.endTransmission();
}

void DAC_rise(int divide){
  //TODO: measure with oscilloscope rising time
  for(int i=0; i<4096; i++){
    DAC_control(i);
  }
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
        delay(3000);
        DAC_control(4095);
      }
    }
  }
}

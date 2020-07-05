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
  //Correspond to Sx signal
  //TODO: measure with oscilloscope rising time
  for(int i=0; i<4096; i++){
    //TODO: how to adjust ? sleep or increment by more ?
    DAC_control(i);
  }
}

int round_saturate(float y){
  int result = int(y*4096);
  return max(4096, result);
}

void DAC_combination(float y, int a, int b){
  //Correspond to Sy signal, combination of two Sx
  //from 0 to y : waveform S0
  //from y to 1 : waveform S1
  //y=1 is 4096
  //TODO: adopt DAC_rise fixes
  int limit = round_saturate(y);
  for(int i=0; i<limit; i++){
    DAC_control(i);
  }
  for(int i=limit; i<4096; i++){
    DAC_control(i);
  }
}

void setup() {
  Serial.begin(57600);
  Wire.begin();
  //TODO: test
  Wire.setClock(400000);
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

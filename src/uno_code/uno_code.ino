#include <SoftwareSerial.h>
#include <Wire.h>

#define MCP4725_ADDR 0x60   

SoftwareSerial mySerial(3, 4);
int i = 0;
float y = 0;
int compteur = 0;
unsigned long time;

void DAC_control(int value){
  Wire.beginTransmission(MCP4725_ADDR);
  Wire.write(64);
  Wire.write(value >> 4);
  Wire.write((value & 15) << 4);
  Wire.endTransmission();
}

void DAC_rise(int factor){
  //Correspond to Sx signal
  //  factor = 1 => 585ms rising time
  //  x = 585/factor ms
  
  int to_add = pow(2, factor-1);
  for(int i=0; i<4096; i += to_add){
    DAC_control(i);
  }
  DAC_control(4095);
}

int round_saturate(float y){
  int result = (int)(y*4096.0);
  return min(4096, result);
}

void DAC_combination(float y, int a, int b){
  //Correspond to Sy signal, combination of two Sx
  //  from 0 to y : waveform S0
  //  from y to 1 : waveform S1
  //  y=1 is 4096

  int limit = round_saturate(y);
  int to_add1 = pow(2, a-1);
  int to_add2 = pow(2, b-1);

  for(int i=0; i<limit; i+=to_add1){
    DAC_control(i);
  }
  for(int i=limit; i<4096; i+=to_add2){
    DAC_control(i);
  }
  DAC_control(4095);
}

void setup() {
  Serial.begin(57600);
  Wire.begin();
  Wire.setClock(400000);
  DAC_control(0);
  
  Serial.println(F("How many rounds"));
  while(!Serial.available()){
    delay(100);
  }
  if (Serial.available()){
    i = Serial.parseInt();
  }

  Serial.println(F("Give y"));
  while(!Serial.available()){
    delay(100);
  }
  if (Serial.available()){
    y = Serial.parseFloat();
    Serial.read();
  }
  delay(1000);
  mySerial.begin(57600);
  DAC_combination(y, 2, 5);
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
          //for (;;);
          asm volatile ("  jmp 0");
        }
        delay(3000);
        DAC_combination(y, 2, 5);
      }
    }
  }
}

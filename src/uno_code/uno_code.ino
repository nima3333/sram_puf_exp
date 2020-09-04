#include <Wire.h>

#define MCP4725_ADDR 0x60   

int i = 0;
int y = 0;
int compteur = 0;
unsigned long time;

void DAC_control(int value){
  // 143us
  Wire.beginTransmission(MCP4725_ADDR);
  Wire.write(64);
  Wire.write(value >> 4);
  Wire.write((value & 15) << 4);
  Wire.endTransmission();
}

void DAC_S64(){
  for(int i=0; i<4096; i += 9){
    DAC_control(i);
  }
  DAC_control(4095);
}

void DAC_S1024(){
  for(int i=0; i<4096; i += 1){
    DAC_control(i);
    delayMicroseconds(107);
  }
  DAC_control(4095);
}

void DAC_Sy(int y){
  for(int i=0; i<y; i += 1){
    DAC_control(i);
    delayMicroseconds(130);
  }
  for(int i=y; i<4096; i += 9){
    DAC_control(i);
  }
  DAC_control(4095);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
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

  Serial.println(F("Give y"));
  while(!Serial.available()){
    delay(100);
  }
  if (Serial.available()){
    y = Serial.parseInt();
    Serial.read();
  }
  delay(500);
  Serial1.begin(57600);
  DAC_Sy(y);
}

void loop() {
  if (Serial1.available()){
    char inByte = Serial1.read();
    if(inByte!='X'){
      Serial.write(inByte);
    }
    else{
      while(!Serial1.available()){}
      char inByte = Serial1.read();
      if(inByte=='X'){
        Serial.flush();
        Serial1.flush();
        DAC_control(1);
        if(++compteur == i){
          for (;;);
          //asm volatile ("  jmp 0");
        }
        delay(1000);
        DAC_Sy(y);
      }
    }
  }
}

#include <SoftwareSerial.h>

SoftwareSerial mySerial(3, 4);
int i = 0;
int compteur = 0;

void setup() {
  Serial.begin(57600);
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
  pinMode(8, OUTPUT);
  digitalWrite(8, HIGH);
}

void loop() {
  if (mySerial.available()){
    char inByte = mySerial.read();
    if(inByte!='X')
      Serial.write(inByte);
    else{
      char inByte = mySerial.read();
      if(inByte=='X'){
        digitalWrite(8, LOW);
        if(++compteur == i){
          for (;;);
        }
        delay(1000);
        digitalWrite(8, HIGH);
      }
    }
  }
}

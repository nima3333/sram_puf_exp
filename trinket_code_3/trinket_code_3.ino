void setup()
{
  Serial.begin( 57600 );
  Serial.println(F("BEGINNING"));
  for(byte* i = 0x800; i<= 0x08FF; i++){
    Serial.print( *i , HEX);
    Serial.print( ' ' );
    delay(1);
  }
  Serial.println(F("XX"));
}

void loop()
{
}

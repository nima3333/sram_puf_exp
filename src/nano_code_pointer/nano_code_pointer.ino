void setup()
{
  uint8_t const * p;
  uint16_t i;

  Serial.begin( 57600 );
  Serial.println(F("BEGINNING"));
  p = RAMSTART;
  i = RAMSTART;
  Serial.println(RAMEND - RAMSTART);
  do
  {
    Serial.print( *p , HEX);
    Serial.print( ' ' );

    ++i;
    ++p;
    
    if ( (i & 0xF) == 0 )
    {
      Serial.println();
    }
    delay(1);
  }
  while ( i != RAMEND );
  Serial.println(F("XX"));
}

void loop()
{
}

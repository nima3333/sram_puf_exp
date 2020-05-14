void setup()
{
  uint8_t const * p;
  uint16_t i;

  Serial.begin( 57600 );
  //Required by the python program to parse
  Serial.println(F("BEGINNING"));
  //RAMSTART / RAMEND macros to designate begining and end of SRAM
  p = RAMSTART;
  i = RAMSTART;
  do
  {
    Serial.print( *p , HEX);
    Serial.print( ' ' );

    ++i;
    ++p;
    
    //Line break every 16 bytes
    if ( (i & 0xF) == 0 )
    {
      Serial.println();
    }
    delay(1);
  }
  while ( i != RAMEND );
  //Required by the python program to parse
  Serial.println(F("XX"));
}

void loop()
{
}

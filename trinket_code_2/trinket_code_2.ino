void setup() {
  Serial.begin( 57600 );
  Serial.println(F("BEGINNING"));
  Serial.println(1024);

  byte someArray[1024];

  for( int i = 1 ; i <= 1024 ; ++i ){
    Serial.print( someArray[ i ], HEX );
    Serial.print( ' ' );
    if ( (i & 0xF) == 0 )
    {
      Serial.println();
    }
    delay(1);  
  }
  Serial.println(F("XX"));
}

void loop() {}

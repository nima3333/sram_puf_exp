uint8_t bytes[ 1024 ] __attribute__ ((section (".noinit"))) __attribute__ ((used));

void setup() {
  Serial.begin( 57600 );
  Serial.println(F("BEGINNING"));
  Serial.println(1024);

  for( int i = 1 ; i <= 1024 ; ++i ){
    Serial.print( bytes[ i ], HEX );
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

void setup() {
  Serial.begin( 57600 );
  //Required by the python program to parse
  Serial.println(F("BEGINNING"));
  Serial.println(1024);

  //Allocate on the stack an array of 1024 bytes
  byte to_print[1024];

  for( int i = 1 ; i <= 1024 ; ++i ){
    Serial.print( to_print[ i ], HEX );
    Serial.print( ' ' );
    if ( (i & 0xF) == 0 )
    {
      Serial.println();
    }
    delay(1);  
  }
  //Required by the python program to parse
  Serial.println(F("XX"));
}

void loop() {}

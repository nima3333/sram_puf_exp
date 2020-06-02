uint8_t * HeapPointer, * StackPointer; // Globally declaring the Stack and Heap pointers.

void setup() {
  Serial.begin( 57600 );
  //Required by the python program to parse
  Serial.println(F("BEGINNING"));
  Serial.println(1024);


  StackPointer = (uint8_t *)malloc(4); //We do a small allocation.
  HeapPointer = StackPointer; // We save the value of the heap pointer.
  free(StackPointer); // We use the dreaded free() to zero the StackPointer.

  for( int i = 1 ; i <= 1024 ; ++i ){
    Serial.print( *(HeapPointer+i), HEX );
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

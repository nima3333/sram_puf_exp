void setup()
{
  Serial.begin( 57600 );

   uint8_t * heapptr, * stackptr;
  stackptr = (uint8_t *)malloc(4);  // use stackptr temporarily
  heapptr = stackptr;                  // save value of heap pointer
  free(stackptr);                        // free up the memory again (sets stackptr to 0)
  stackptr =  (uint8_t *)(SP);       // save value of stack pointer
  Serial.println(F("BEGINNING"));
  Serial.println(RAMSTART);
  Serial.println(RAMEND);
  Serial.println ((int) stackptr);
  Serial.println ((int) heapptr);


}

void loop()
{
}

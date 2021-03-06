#include<SPI.h>
#include<nRF24L01.h>
#include<RF24.h>
const uint64_t pipe[1]= {0xF0F0F0F0E1LL};
RF24 radio(9,10);
int rec[1] = {0};
int vel[2];
void setup()
{
  Serial.begin(57600);
  radio.begin();
  delay(100);
  radio.setAutoAck(true);
  radio.enableAckPayload();
  radio.enableDynamicPayloads();
  radio.openReadingPipe(1,pipe[0]);
  radio.startListening();
  radio.setRetries(15,15);
}
void loop()
{
  if ( radio.available() ) {
    radio.writeAckPayload( 1, rec, sizeof(int) );
    radio.read( &vel,sizeof(vel) );rec[0]+=1;
    Serial.print("vel value got is : ");
    Serial.print(vel[0]);
    Serial.print(" ");
    Serial.println(vel[1]);
  }
}

#include<SPI.h>
#include<nRF24L01.h>
#include<RF24.h>
#include <ros.h>
#include <geometry_msgs/Point.h>

int msg[2]={0,0};
int rec[1] = {0};
bool stat = false;
RF24 radio(9,10);
const uint64_t pipe[1] = {0xF0F0F0F0E1LL};
  
ros::NodeHandle  nh;
void velControl(const geometry_msgs::Point& vel){
  msg[0]=vel.x;
  msg[1]=vel.y;
  stat=true;

}


ros::Subscriber<geometry_msgs::Point> motor("motor_vel", &velControl );

void setup()
{
  Serial.begin(57600);
  radio.begin();
  delay(100);
  radio.setAutoAck(true);
  radio.enableAckPayload();
  radio.enableDynamicPayloads();
  radio.stopListening();
  radio.openWritingPipe(pipe[0]);
  radio.setRetries(15,15);
  nh.initNode();
  nh.subscribe(motor);
 }
void loop()
{  nh.spinOnce();
   delay(0);
  if(stat)
  {
    if(radio.write(msg,sizeof(msg)))
    {
      //Serial.print( msg[0] );
      //Serial.println("...tx success");
      if(radio.isAckPayloadAvailable())
      {
        radio.read(rec,sizeof(int));
        //Serial.print("received ack payload is : ");
        //Serial.println(rec[0]);
      }
      else
      {
        stat = false; //doing this completely shuts down the transmitter if an ack payload is not received !!
        //Serial.println("status has become false so stop here....");
      }
    }
  }
}

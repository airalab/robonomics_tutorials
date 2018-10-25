#include <ros.h>
#include <std_msgs/Empty.h>

ros::NodeHandle  nh;

void blink(int led, int mil) {

  digitalWrite(led, HIGH);
  delay(mil);
  digitalWrite(led, LOW);
  delay(mil);

}

void messageCb( const std_msgs::Empty& toggle_msg){
  blink(LED_BUILTIN, 500);
  blink(LED_BUILTIN, 500);
  blink(LED_BUILTIN, 500);
}

ros::Subscriber<std_msgs::Empty> sub("blink_led", &messageCb );

void setup()
{ 
  pinMode(LED_BUILTIN, OUTPUT);
  nh.initNode();
  nh.subscribe(sub);
}

void loop()
{  
  nh.spinOnce();
  delay(1);
}

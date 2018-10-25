#include <ros.h>
#include <std_msgs/Empty.h>

ros::NodeHandle nh;

void blink(int led, int mil) {

  digitalWrite(led, HIGH);
  delay(mil);
  digitalWrite(led, LOW);
  delay(mil);

}

void blinkRedCb(const std_msgs::Empty& msg) {
  blink(13, 500);
  blink(13, 500);
  blink(13, 500);
}

void blinkBlueCb(const std_msgs::Empty& msg) {
  blink(12, 500);
  blink(12, 500);
  blink(12, 500);
}

ros::Subscriber<std_msgs::Empty> subRed("blink_red", &blinkRedCb);
ros::Subscriber<std_msgs::Empty> subBlue("blink_blue", &blinkBlueCb);

void setup()
{
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);

  nh.initNode();
  nh.subscribe(subRed);
  nh.subscribe(subBlue);
}

void loop()
{
  nh.spinOnce();
  delay(1);
}

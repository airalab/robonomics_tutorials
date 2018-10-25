#include <MQ2.h>
#include <MQ7.h>
#include <TroykaMQ.h>
#include <BaseMQ.h>

#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif
#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle nh;

std_msgs::String data_str;
ros::Publisher measurements("measurements", &data_str);

#define INTERVAL_GET_DATA 5000  // интервала измерений, мс 
// пин, к которому подключен датчик
#define MQ7PIN A1
// создаём объект для работы с датчиком
MQ7 mq7(MQ7PIN);
//имя для пина, к которому подключен датчик
#define PIN_MQ2 A0
// создаём объект для работы с датчиком и передаём ему номер пина
MQ2 mq2(PIN_MQ2);

// dust sensor
int measurePin = A5;
int ledPower = 12;

float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

unsigned int samplingTime = 280;
unsigned int deltaTime = 40;
unsigned int sleepTime = 9680;

unsigned long millis_int1=0;
 
void setup()
{
  pinMode(ledPower,OUTPUT);
  // перед калибровкой датчика прогрейте его 60 секунд
  // выполняем калибровку датчика на чистом воздухе
  mq2.calibrate();
  mq7.calibrate();
  mq7.getRo();

  nh.initNode();
  nh.advertise(measurements);  
}
 
void loop()
{
  if(millis()-millis_int1 >= INTERVAL_GET_DATA) {
    getDustData();

    String data = "";
    data = data + String(dustDensity) + " ";
    data = data + String(mq7.readCarbonMonoxide()) + " ";
    data = data + String(mq2.readLPG()) + " ";
    data = data + String(mq2.readMethane()) + " ";
    data = data + String(mq2.readSmoke()) + " ";
    data = data + String(mq2.readHydrogen());
    
    data_str.data = data.c_str();
    measurements.publish(&data_str);

    delay(100);
    // старт интервала отсчета
    millis_int1=millis();
  }

  nh.spinOnce();
}

void getDustData() {
  digitalWrite(ledPower,LOW);
  delayMicroseconds(samplingTime);

  voMeasured = analogRead(measurePin);

  delayMicroseconds(deltaTime);
  digitalWrite(ledPower,HIGH);
  delayMicroseconds(sleepTime);

  calcVoltage = voMeasured*(5.0/1024);
  dustDensity = 0.17*calcVoltage-0.1;

  if ( dustDensity < 0)
  {
    dustDensity = 0.00;
  }
}

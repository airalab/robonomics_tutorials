String inputString = "";
boolean stringComplete = false;

//use some wiring from this pin to reset pin to disable auto-reset
int resetPin = 8;

//Check if inputString match the given cmd string
bool cmd(String cmd) {
  if (inputString.startsWith(cmd)) {
    return true;
  } else {
    return false;
  }
}

//Simply blink the led for some time
void blink(int led, int mil) {

  digitalWrite(led, HIGH);
  delay(mil);
  digitalWrite(led, LOW);
  delay(mil);

}

//This function will restart your board
void(* reboot) (void) = 0;

void setup() {
  //Set the serial port speed
  Serial.begin(9600);
  inputString.reserve(255);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);

  //with some wiring from the resetPin (pin 8) to the reset pin, this will disable auto-restart
  digitalWrite(resetPin, HIGH);

  //blink 3 times to show that system is starting
  blink(13, 500);
  blink(13, 500);
  blink(13, 500);
}

//Perform actions based on the input
void check_input(String input) {
  // Turn red led on
  if (cmd("red")) {
    blink(13, 500);
    blink(13, 500);
    blink(13, 500);

  // Turn blue led on
  } else if(cmd("blue")) {
    blink(12, 500);
    blink(12, 500);
    blink(12, 500);
    
  // Call reboot
  } else if (cmd("reboot")) {
    Serial.println("Rebooting...");
    delay(200);
    reboot();
  } 

  stringComplete = false;
  inputString = "";
}

//The main loop function
void loop() {
  serialEvent();
  if (stringComplete) {
    // Call our input handler function
    check_input(inputString);
  }
}

//This function works when we have data comming from the serial port
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if ( inChar == '\b') {
      inputString.remove(inputString.length() - 1, inputString.length());
    } else if ( int(inChar) == 13 ) {
      inChar = '\n';
    } else {
      //add current character to input command
      inputString += inChar;
    }

    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

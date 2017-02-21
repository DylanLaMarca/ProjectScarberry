/*
  Frequency Trigger:
      Triggers a camera to take a number of photos specified over serial and
    flashes an stobe light a specified number of times per photo for a specified
    duration.
  Outputs (+5v):
    ~ pin 12: Ximea Camera xiQ MQ022RG-CM Trigger Cable Digital Input (VDI) 
    ~ pin 11: IR Strobe Curcuit Optic Isolator
 ************************************************
  Created:  4/8/2016
    Dylan Michael LaMarca [dylan@lamarca.org]
  Modified: 21/2/2017
    Dylan Michael LaMarca [dylan@lamarca.org]
  Github:
    https://github.com/GhoulPoP/ProjectScarberry
*/

unsigned long strobe_trigger_time = 0;
unsigned long frame_trigger_time = 0;
bool start = 0;

int frame_rate;
int strobe_rate;
float duty_cycle;

unsigned long frame_time;
unsigned long strobe_time;
unsigned long strobe_time_high;

/*
  Summary:
    Initializes the arduinos operation by setting pins 13 - 9 
    as digital output and pin 8 as digital input, obtaining
    values for frame_rate, strobe_rate, and duty_cycle over serial,
    calculating frame_time, strobe_time, and strobe_high_time, and
    then waiting for a serial input of 1 to start loop.
*/
void setup() {
  DDRB = B11111110;
  Serial.begin(115200);
  Serial.setTimeout(1000);
  frame_rate = getSerialValue();
  strobe_rate = getSerialValue();
  duty_cycle = getSerialValue();
  frame_time = 1000000/frame_rate;
  strobe_time = frame_time/strobe_rate;
  strobe_time_high = strobe_time*(1.0-duty_cycle);
  printAllVariables();
  while(!start) {
    if(Serial.available()) {
      if(Serial.parseFloat() == 1) {
        start = 1;
      }
    }
  }
  Serial.println("Start!!");
}

/*
  Summary:
    Loops until a float higher than zero is recieved.
  Return:
    float value:
      A float value recieved over serial greater than 0
*/
float getSerialValue() {
  float value = 0;
  while(value <= 0) {
    if(Serial.available()) {
      value = Serial.parseFloat();
    }
  }
  //delay(1000);
  Serial.println(9);
  return value;
}

/*
  Summary:
    Continuously repeats, testing to see if the current time 
    (in microseconds) is equal to frame_trigger_time,
    strobe_trigger_time, or strobe_trigger_time - strobe_time_high.
    If micros is equal or higher than frame_trigger_time
    frame_trigger-time is incramented by frame_time and pin 12
    is set to high. The same is done to strobe_trigger_time but is incramented
    by strobe_time and sets pin 11 to high. If micros is equal to 
    strobe_trigger_time-strobe_time_high pins 13-9 are set to low.
*/
void loop() {
  if(micros() >= frame_trigger_time) {
    frame_trigger_time += frame_time;
    digitalWrite(12,HIGH);
  }
  if(micros() >= strobe_trigger_time) {
    strobe_trigger_time += strobe_time;
    digitalWrite(11,HIGH);
  } else if(micros() >= strobe_trigger_time-strobe_time_high) {
    PORTB = B11000000;
  }
}

/*
  Summary:
    Continuously repeats, testing to see if
    there is any serial input, if there is and
    it is equal to 4 pins 13-9 are set to low
    and the arduino is stopped by a while true
    loop.
*/
void serialEvent() {
  if(Serial.available()) {
    Serial.setTimeout(0);
    if(Serial.parseInt() == 4) {
      PORTB = B11000000;
      while(1){}
    }
    Serial.setTimeout(100);
  }
}

/*
  Summary:
    Prints all of the global variables in the sketch.
*/
void printAllVariables() {
  printVariable("FrameRate: ",frame_rate);
  printVariable("StrobeRate: ",strobe_rate);
  printVariable("DutyCycle: ",duty_cycle);
  printVariable("FrameTime: ",frame_time);
  printVariable("StrobeTime: ",strobe_time);
  printVariable("StrobeTimeHigh: ",strobe_time_high);
}

/*
  Summary:
    Prints a float value and a string next to one another to Serial.
  Example:
    printVariable('Hello: ',70)
    Serial = 'Hello: 70'
  Parameters:
    String title:
      The string which prints in front of the float
    float value:
      The float which prints after the string
*/
void printVariable(String title, float value) {
  Serial.print(title);
  Serial.print(value);
  Serial.println();
}



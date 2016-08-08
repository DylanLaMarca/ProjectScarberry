unsigned long strobe_trigger_time = 0;
unsigned long frame_trigger_time = 0;
bool start = 0;

int frame_rate;
int strobe_rate;
float duty_cycle;

unsigned long frame_time;
unsigned long strobe_time;
unsigned long strobe_time_high;


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

float getSerialValue() {
  float value = 0;
  while(value <= 0) {
    if(Serial.available()) {
      value = Serial.parseFloat();
    }
  }
  return value;
}

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

void printAllVariables() {
  printVariable("FrameRate: ",frame_rate);
  printVariable("StrobeRate: ",strobe_rate);
  printVariable("DutyCycle: ",duty_cycle);
  printVariable("FrameTime: ",frame_time);
  printVariable("StrobeTime: ",strobe_time);
  printVariable("StrobeTimeHigh: ",strobe_time_high);
}

void printVariable(String title, float value) {
  Serial.print(title);
  Serial.print(value);
  Serial.println();
}



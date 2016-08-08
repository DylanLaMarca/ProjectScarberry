unsigned long strobe_trigger_time;
unsigned long frame_trigger_time = 0;
bool start = 0;
int loop_count = 0;

int frame_rate;
int strobe_rate;
float duty_cycle;
int start_value;
int reset_value;
int end_value;

unsigned long frame_time;
unsigned long strobe_time;
unsigned long strobe_time_high;


void setup() {
  digitalWrite(10,HIGH);
  DDRB = B11111110;
  Serial.begin(115200);
  Serial.setTimeout(1000);
  frame_rate = getSerialValue();
  strobe_rate = getSerialValue();
  duty_cycle = getSerialValue();
  start_value = getSerialValue();
  reset_value = getSerialValue();
  end_value = getSerialValue();
  frame_time = 1000000/frame_rate;
  strobe_time = frame_time/strobe_rate;
  strobe_time_high = strobe_time*(1.0-duty_cycle);
  printAllVariables();
  while(!start) {
    if(Serial.available()) {
      if(Serial.parseFloat() == start_value) {
        start = 1;
      }
    }
  }
  Serial.println("Start!!");
  frame_trigger_time = micros();
}

float getSerialValue() {
  float value = 0;
  while(value <= 0.0) {
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
    loop_count++;
  }
  if(micros() >= strobe_trigger_time) {
    strobe_trigger_time += strobe_time;
    digitalWrite(11,HIGH);
  } else if(micros() >= strobe_trigger_time-strobe_time_high) {
    PORTB = B11000100;
  }
}

void serialEvent() {
  if(Serial.available()) {
    Serial.setTimeout(0);
    int parsed_int = Serial.parseInt();
    if(parsed_int == reset_value) {
      PORTB = B11000100;
      printVariable("count: ",loop_count);
      while(1){}
    } else if(parsed_int == end_value) {
      digitalWrite(10,LOW);
      printVariable("count: ",loop_count);
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
  printVariable("StartValue: ",start_value);
  printVariable("ResetValue: ",reset_value);
  printVariable("EndValue: ",end_value);
}

void printVariable(String title, float value) {
  Serial.print(title);
  Serial.print(value);
  Serial.println();
}



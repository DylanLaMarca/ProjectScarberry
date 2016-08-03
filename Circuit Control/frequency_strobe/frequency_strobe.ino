bool use_microseconds = true;
double duty_cycle = -1;
int trigger = -1;
int hertz = -1;
long time_high;
long time_low;
long period;

void setup() {
  DDRB = B11111111;
  
  Serial.begin(115200);
  hertz = getSerialValue(hertz);
  while (duty_cycle <= 0 || duty_cycle > 1) {
    if (Serial.available() > 0) {
      duty_cycle = Serial.parseFloat();
    }
  }
  trigger = getSerialValue(trigger);
  
  if(1000000/hertz <= 16383) {
    period = 1000000/hertz;
  } else {
    use_microseconds = false;
    period = 1000/hertz;
  }
  time_high = period*duty_cycle;
  time_low = period-time_high;
  Serial.print(period);
  Serial.print(",");
  Serial.print(time_high);
  Serial.println();
  Serial.println(use_microseconds);
}

float getSerialValue(int value) {
  while (value < 1) {
    if (Serial.available() > 0) {
      value = Serial.parseFloat();
    }
  }
  return value;
}

void loop() {
  if(use_microseconds) {
      micro_loop();
  } else {
    while(true){
      milli_loop();
    }
  }
}

void micro_loop() {
  while(true){
    pinMode(12,HIGH);
    for(int count = 0; count < trigger; count++) {
      pinMode(13,HIGH);
      delayMicroseconds(time_high);
      PORTB = B11111111;
      delayMicroseconds(time_low);
    }
  }
}

void milli_loop() {
  while(true){
    digitalWrite(12,HIGH);
    for(int count = 0; count < trigger; count++) {
      digitalWrite(13,HIGH);
      delay(time_high);
      PORTB = B11000000;
      delay(time_low);
    }
  }
}

void delayStrobe(int delay_time) {
  if(use_microseconds) {
    delayMicroseconds(delay_time);
  } else {
    delay(delay_time);
  }
}

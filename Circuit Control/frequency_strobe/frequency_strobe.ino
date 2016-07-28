int hertz;
int period;
double duty_cycle;
int time_high;


void setup() {
  pinMode(13, OUTPUT);
  hertz = 10;
  duty_cycle = .5;
  period = 1000/hertz;
  time_high = period*duty_cycle;
}

void loop() {
  digitalWrite(13, HIGH);  
  Serial.print("On");
  delay(time_high);
  digitalWrite(13, LOW);  
  Serial.print("Off");
  delay(period-time_high);
}

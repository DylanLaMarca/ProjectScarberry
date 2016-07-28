int TOTAL_MILLISECONDS = 1000;
int hertz;
double thigh;
int tcycle;
double duty_cycle;


void setup() {
  pinMode(13, OUTPUT);
  hertz = 1;
  duty_cycle = .5;
  calc_duty_cycle();
}

void calc_duty_cycle() {
  tcycle = TOTAL_MILLISECONDS/hertz;
  thigh = tcycle*duty_cycle;
}

void loop() {
  digitalWrite(13, HIGH);  
  delay(thigh);
  digitalWrite(13, LOW);  
  delay(tcycle-thigh);
}

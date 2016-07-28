int hertz = -1;
int period;
double duty_cycle = -1;
int time_high;


void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  //hertz = 1;
  //duty_cycle = .5;
  bool start_loop = false;
  String inputString = "";
  while (hertz < 1) {
    if (Serial.available() > 0) {
      hertz = Serial.parseFloat();
    }
  }
  while (duty_cycle <= 0 || duty_cycle > 1) {
    if (Serial.available() > 0) {
      duty_cycle = Serial.parseFloat();
    }
  }
  Serial.println(hertz);
  Serial.println(duty_cycle);
  period = 1000/hertz;
  Serial.println(period);
  time_high = period*duty_cycle;
  Serial.println(time_high);
}

void loop() {
  digitalWrite(13, HIGH);  
  Serial.println("On");
  delay(time_high);
  digitalWrite(13, LOW);  
  Serial.println("Off");
  delay(period-time_high);
}

/*void serialEvent() {
  while (Serial.available()) {
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13,LOW);
    delay(1000);
  }
}*/

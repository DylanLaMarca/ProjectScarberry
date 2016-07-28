int TOTAL_MICROSECOND = 1000000;
int hertz;
double thigh;
double tcycle;


void setup() {
  pinMode(13, OUTPUT);
  Hertz = 20;
  
}

void loop() {
  digitalWrite(13, HIGH);  
  delay(1000);              // wait for a second
  digitalWrite(13, LOW);  
  delay(1000);              // wait for a second
}

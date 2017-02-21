void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(12,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(12,HIGH);
  Serial.println("On");
  delay(1500);
  digitalWrite(12,LOW);
  Serial.println("Off");
  delay(1500);
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

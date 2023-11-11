#define BUTTON 33
#define CAMERA_PIN 32

volatile bool pressed = false;
const int debounceDelay = 100; // Adjust this value for "delay"
volatile unsigned long lastDebounceTime = 0;

void IRAM_ATTR isr() {
  unsigned long currentTime = millis();
  if (currentTime - lastDebounceTime > debounceDelay) {
    pressed = !pressed;
  }
  lastDebounceTime = currentTime;
}

void setup() {
  Serial.begin(115200);
  //Button
  pinMode(BUTTON, INPUT_PULLUP);
  attachInterrupt(BUTTON, isr, FALLING);
  //Camera
  pinMode(CAMERA_PIN, OUTPUT);
  digitalWrite(CAMERA_PIN, LOW);
}

void loop() {
  if (pressed) {
    digitalWrite(CAMERA_PIN,HIGH);
    delay(1000);
    digitalWrite(CAMERA_PIN,LOW);
    pressed = false;
  }   
}

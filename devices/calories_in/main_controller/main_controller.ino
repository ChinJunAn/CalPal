// Button pin
/*
#define BUTTON_PIN GPIO_NUM_27 //for waking from deep sleep with external trigger
#define BUTTON_PIN_INT 27 //for other usage of button
#define CAMERA_PIN 33

void print_wakeup_reason(){
  esp_sleep_wakeup_cause_t wakeup_reason;

  wakeup_reason = esp_sleep_get_wakeup_cause();

  switch(wakeup_reason)
  {
    case ESP_SLEEP_WAKEUP_EXT0 : Serial.println("Wakeup caused by external signal using RTC_IO"); break;
    case ESP_SLEEP_WAKEUP_EXT1 : Serial.println("Wakeup caused by external signal using RTC_CNTL"); break;
    case ESP_SLEEP_WAKEUP_TIMER : Serial.println("Wakeup caused by timer"); break;
    case ESP_SLEEP_WAKEUP_TOUCHPAD : Serial.println("Wakeup caused by touchpad"); break;
    case ESP_SLEEP_WAKEUP_ULP : Serial.println("Wakeup caused by ULP program"); break;
    default : Serial.printf("Wakeup was not caused by deep sleep: %d\n",wakeup_reason); break;
  }
}
*/
void setup() {
  /*
  Serial.begin(115200);
  delay(1000);
  print_wakeup_reason();

  // Button setup
  pinMode(BUTTON_PIN_INT, INPUT_PULLUP);
  esp_sleep_enable_ext0_wakeup(BUTTON_PIN, LOW);

  // Camera setup
  pinMode(CAMERA_PIN, OUTPUT);
  digitalWrite(CAMERA_PIN, LOW);
  Serial.println("Setup done");

  Serial.println("Taking picture");
  digitalWrite(CAMERA_PIN, HIGH);
  delay(10000);
  digitalWrite(CAMERA_PIN, LOW);
  delay(1000);
  Serial.println("Picture taken, going to sleep now");
  esp_deep_sleep_start();
  Serial.println("This should not appear");
  */
}

void loop() {
  //test sleep
  delay(30000);
  esp_deep_sleep_start();
}

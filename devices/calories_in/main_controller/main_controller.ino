#include "Arduino.h"
#include <WiFi.h>
#include "ESP32MQTTClient.h"
const char* ssid = "CJA";
const char* password = "qwertyuiop";
char *server = "mqtt://192.168.97.192:1883";
char *subscribeTopic = "foo";
char *publishTopic = "ci/weight";
ESP32MQTTClient mqttClient;

#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif
//weigh pins:
const int HX711_dout = 14; //mcu > HX711 dout pin
const int HX711_sck = 12; //mcu > HX711 sck pin
//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);
const int calVal_calVal_eepromAdress = 0;
unsigned long t = 0;

#define BUTTON 32
#define CAMERA_PIN 33

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

void connectMQTT() {
  WiFi.begin(ssid, password);
  WiFi.setHostname("c3test");
  while(WiFi.status() != WL_CONNECTED) {
    Serial.println("connecting...");
    delay(1000);
  }
  Serial.println("connected");
  mqttClient.loopStart();
}

void sendData(String weight) {
  Serial.println("Sending weight");
  Serial.println(weight);
  mqttClient.publish(publishTopic, weight, 0, false);
  Serial.println("Weight sent");
  delay(2000);
  mqttClient.setConnectionState(false);
  WiFi.disconnect();
}

void setup() {
  Serial.begin(115200);
  //Button
  pinMode(BUTTON, INPUT_PULLUP);
  attachInterrupt(BUTTON, isr, FALLING);
  //Camera
  pinMode(CAMERA_PIN, OUTPUT);
  digitalWrite(CAMERA_PIN, LOW);
  //Weight
  LoadCell.begin();
  unsigned long stabilizingtime = 2000; // tare preciscion can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
  }
  else {
    LoadCell.setCalFactor(-401.49); // set calibration factor (float)
    Serial.println("Startup is complete");
  }
  while (!LoadCell.update());
  //MQTT
  log_i();
  log_i("setup, ESP.getSdkVersion(): ");
  log_i("%s", ESP.getSdkVersion());
  mqttClient.enableDebuggingMessages();
  mqttClient.setURI(server);
  mqttClient.enableLastWillMessage("lwt", "I am going offline");
  mqttClient.setKeepAlive(30);
  mqttClient.disableAutoReconnect();
}

void loop() {
  static boolean newDataReady = 0;
  const int serialPrintInterval = 50; 
  if (LoadCell.update()) newDataReady = true;
  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
      float i = LoadCell.getData();
      newDataReady = 0;
      t = millis();
      if (pressed) {
        connectMQTT();
        delay(1000);
        sendData(String(i));

        Serial.println("Taking picture");
        digitalWrite(CAMERA_PIN,HIGH);
        delay(1000);
        digitalWrite(CAMERA_PIN,LOW);
        pressed = false;
      } 
    }
  }
}

void onConnectionEstablishedCallback(esp_mqtt_client_handle_t client) {
    if (mqttClient.isMyTurn(client)) // can be omitted if only one client
    {
        mqttClient.subscribe(subscribeTopic, [](const String &payload)
                             { log_i("%s: %s", subscribeTopic, payload.c_str()); });

        mqttClient.subscribe("bar/#", [](const String &topic, const String &payload)
                             { log_i("%s: %s", topic, payload.c_str()); });
    }
}

esp_err_t handleMQTT(esp_mqtt_event_handle_t event) {
    mqttClient.onEventCallback(event);
    return ESP_OK;
}

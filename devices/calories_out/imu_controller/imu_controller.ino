#include "Arduino.h"
#include <WiFi.h>
#include "ESP32MQTTClient.h"

#include <Wire.h>
#include <MPU6050.h>

const char* ssid = "CJA";
const char* password = "qwertyuiop";
char *server = "mqtt://192.168.97.192:1883";
char *subscribeTopic = "foo";
char *publishTopic = "esp/imu";
ESP32MQTTClient mqttClient; // all params are set later

#define BUTTON 4
volatile bool pressed = false;
const int debounceDelay = 100; // Adjust this value for "delay"
volatile unsigned long lastDebounceTime = 0;

MPU6050 mpu;
int16_t gx, gy, gz, ax, ay, az;
String globalData = "";

void IRAM_ATTR isr() {
  unsigned long currentTime = millis();
  if (currentTime - lastDebounceTime > debounceDelay) {
    pressed = !pressed;
  }
  lastDebounceTime = currentTime;
}

void recordData() {
  mpu.getMotion6(&gx, &gy, &gz, &ax, &ay, &az);
  String data = String(millis()) + "," + String(gx) + "," + String(gy) + "," + String(gz) + "," + String(ax) + "," + String(ay) + "," + String(az);
  globalData += data + "\n";
}

void connectMQTT() {
  WiFi.begin(ssid, password);
  WiFi.setHostname("c3test");
  while(WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting..");
    delay(1000);
  }
  mqttClient.loopStart();
}

int pubCount = 0;
void sendData() {
  Serial.println("Button pressed, sending data...");
  mqttClient.publish(publishTopic, globalData, 0, false);
  delay(2000);
  mqttClient.setConnectionState(false);
  WiFi.disconnect();
}

void setup() {
  Serial.begin(115200);
  //button
  pinMode(BUTTON, INPUT_PULLUP);
  attachInterrupt(BUTTON, isr, FALLING);
  //imu
  Wire.begin();
  mpu.initialize();
  //mqtt
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
  recordData();
  if (pressed) {
    connectMQTT();
    delay(1000);
    sendData();
    pressed = false;
  }   
  delay(500);
}

void onConnectionEstablishedCallback(esp_mqtt_client_handle_t client)
{
    if (mqttClient.isMyTurn(client)) // can be omitted if only one client
    {
        mqttClient.subscribe(subscribeTopic, [](const String &payload)
                             { log_i("%s: %s", subscribeTopic, payload.c_str()); });

        mqttClient.subscribe("bar/#", [](const String &topic, const String &payload)
                             { log_i("%s: %s", topic, payload.c_str()); });
    }
}

esp_err_t handleMQTT(esp_mqtt_event_handle_t event)
{
    mqttClient.onEventCallback(event);
    return ESP_OK;
}

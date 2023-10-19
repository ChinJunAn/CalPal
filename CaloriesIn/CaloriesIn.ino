#include "Arduino.h"
#include <WiFi.h>
#include "ESP32MQTTClient.h"
const char *ssid = "CJA";
const char *pass = "qwertyuiop";
char *server = "mqtt://192.168.39.192:1883";
char *subscribeTopic = "actuation/laptop";
char *publishTemp = "pic/esp";
ESP32MQTTClient mqttClient; // all params are set later

const int buttonPin = 2; // Replace with your button's GPIO pin
volatile bool buttonState = LOW; // Initial state of the button
volatile unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 50; // Adjust this value as needed

//image
String messageString = "fake image";
size_t messageLength = messageString.length(); // Use length() to get the string length
unsigned char* messageBytes = (unsigned char*)messageString.c_str(); // Convert to byte array

void buttonInterrupt() {
  unsigned long currentMillis = millis();
  if (currentMillis - lastDebounceTime > debounceDelay) {
    lastDebounceTime = currentMillis;
    int buttonReading = digitalRead(buttonPin);
    if (buttonReading != buttonState) {
      buttonState = buttonReading;
      if (buttonState == LOW) {
        // Button pressed
        Serial.println("sending picture");
        mqttClient.publish(publishTemp, messageBytes, 0, false); //insert byte array of images
      } else {
        // Button released
      }
    }
  }
}

void setup() {
  Serial.begin(115200);

  //set up for MQTT client
  log_i();
  log_i("setup, ESP.getSdkVersion(): ");
  log_i("%s", ESP.getSdkVersion());
  mqttClient.enableDebuggingMessages();
  mqttClient.setURI(server);
  mqttClient.enableLastWillMessage("lwt", "I am going offline");
  mqttClient.setKeepAlive(30);
  WiFi.begin(ssid, pass);
  WiFi.setHostname("c3test");
  while(WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.print('Connected');
  mqttClient.loopStart();

  //set up button
  pinMode(buttonPin, INPUT_PULLUP); // Enable internal pull-up resistor
  attachInterrupt(digitalPinToInterrupt(buttonPin), buttonInterrupt, CHANGE);
}

void loop() {
  // Your main loop code here
}

void onConnectionEstablishedCallback(esp_mqtt_client_handle_t client)
{
    if (mqttClient.isMyTurn(client)) // can be omitted if only one client
    {
        mqttClient.subscribe(subscribeTopic, [](const String &payload)
                             {
                              //classifier = String(payload.c_str()); 
                             });
    }
}

esp_err_t handleMQTT(esp_mqtt_event_handle_t event)
{
    mqttClient.onEventCallback(event);
    return ESP_OK;
}
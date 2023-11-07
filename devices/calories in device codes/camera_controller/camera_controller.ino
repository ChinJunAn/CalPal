#include <WiFi.h>
#include "esp_camera.h"
#include "esp_timer.h"
#include "img_converters.h"
#include "Arduino.h"
#include "soc/soc.h"           // Disable brownour problems
#include "soc/rtc_cntl_reg.h"  // Disable brownour problems
#include "driver/rtc_io.h"
#include <SPIFFS.h>
#include <FS.h>
#include "ESP32MQTTClient.h"

const char* ssid = "CJA";
const char* password = "qwertyuiop";
char *server = "mqtt://192.168.97.192:1883";
char *subscribeTopic = "foo";
char *publishTopic = "esp/cam";
ESP32MQTTClient mqttClient; 

// OV2640 camera module pins (CAMERA_MODEL_AI_THINKER)
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22
// LED pin
#define FLASH 4
#define CAMERA_PIN 13

camera_config_t camera_config = {
  .pin_pwdn = PWDN_GPIO_NUM,
  .pin_reset = RESET_GPIO_NUM,
  .pin_xclk = XCLK_GPIO_NUM,
  .pin_sscb_sda = SIOD_GPIO_NUM,
  .pin_sscb_scl = SIOC_GPIO_NUM,
  .pin_d7 = Y9_GPIO_NUM,
  .pin_d6 = Y8_GPIO_NUM,
  .pin_d5 = Y7_GPIO_NUM,
  .pin_d4 = Y6_GPIO_NUM,
  .pin_d3 = Y5_GPIO_NUM,
  .pin_d2 = Y4_GPIO_NUM,
  .pin_d1 = Y3_GPIO_NUM,
  .pin_d0 = Y2_GPIO_NUM,
  .pin_vsync = VSYNC_GPIO_NUM,
  .pin_href = HREF_GPIO_NUM,
  .pin_pclk = PCLK_GPIO_NUM,
  .xclk_freq_hz = 20000000,  // Adjust the frequency as needed
  .ledc_timer = LEDC_TIMER_0,
  .ledc_channel = LEDC_CHANNEL_0,
  .pixel_format = PIXFORMAT_JPEG, // Adjust as needed
  .frame_size = FRAMESIZE_SVGA,   // Adjust as needed
  .jpeg_quality = 10,            // Adjust as needed (0-63)
  .fb_count = 2                   // Double buffer
};

void flashOn() {
  digitalWrite(FLASH, HIGH); 
  // Set the FLASH pin to HIGH to turn on the LED flash
}

// Function to turn off the LED flash
void flashOff() {
  digitalWrite(FLASH, LOW); 
  // Set the FLASH pin to LOW to turn off the LED flash
}

void captureAndSendPhoto() {
  camera_fb_t* fb = esp_camera_fb_get();  
  delay(1000);//This is key to avoid an issue with the image being very dark and green. If needed adjust total delay time.
  flashOn();
  fb = esp_camera_fb_get();
  delay(1000);
  flashOff();
  String imageBase64 = base64_encode(fb->buf, fb->len);
  mqttClient.publish(publishTopic, imageBase64);
  esp_camera_fb_return(fb);
  //esp_deep_sleep_start();
}

void setup() {
  Serial.begin(115200);
  pinMode(FLASH, OUTPUT);
  pinMode(CAMERA_PIN, INPUT_PULLUP);
  esp_camera_init(&camera_config); 

  flashOn();
  delay(500);
  flashOff();

  log_i();
  log_i("setup, ESP.getSdkVersion(): ");
  log_i("%s", ESP.getSdkVersion());
  mqttClient.enableDebuggingMessages();
  mqttClient.setURI(server);
  mqttClient.enableLastWillMessage("lwt", "I am going offline");
  mqttClient.setKeepAlive(30);
  WiFi.begin(ssid, password);
  WiFi.setHostname("c3test");
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
  mqttClient.loopStart();
  captureAndSendPhoto();
}

void loop() {
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

String base64_encode(const uint8_t* data, size_t length) {
  const char base64Chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  String encoded;
  int i = 0;
  
  while (i < length) {
    // Read the first 8-bit chunk
    uint8_t octet_a = i < length ? data[i++] : 0;
    uint8_t octet_b = i < length ? data[i++] : 0;
    uint8_t octet_c = i < length ? data[i++] : 0;
    
    // Combine the 8-bit chunks into a 24-bit group
    uint32_t triple = (octet_a << 16) + (octet_b << 8) + octet_c;
    
    // Break the 24-bit group into four 6-bit chunks and append base64 characters
    encoded += base64Chars[(triple >> 18) & 63];
    encoded += base64Chars[(triple >> 12) & 63];
    encoded += base64Chars[(triple >> 6) & 63];
    encoded += base64Chars[triple & 63];
  }
  
  // Add padding if necessary
  while (length % 3 != 0) {
    encoded += '=';
    length++;
  }
  
  return encoded;
}

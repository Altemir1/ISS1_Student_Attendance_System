#include <WiFi.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN      5   // ESP32 pin GPIO5 
#define RST_PIN     27  // ESP32 pin GPIO27 
#define BUZZER_PIN  17  // ESP32 pin GPIO17 for buzzer

MFRC522 rfid(SS_PIN, RST_PIN);
const char* WIFI_SSID = "TechnoPark";
const char* WIFI_PASSWORD = "techno2020";
const char* HOST_NAME = "http://192.168.1.226"; // Change to your PC's IP address
const char* PATH_NAME = "/reg_uid.php";

void setup() {
  Serial.begin(9600);
  SPI.begin(); // Initialize SPI bus
  rfid.PCD_Init(); // Initialize MFRC522
  
  pinMode(BUZZER_PIN, OUTPUT); // Set the buzzer pin as output
  
  Serial.println("Tap an RFID/NFC tag on the RFID-RC522 reader");
  
  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.println("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to Wi-Fi");
  
  // Initialize LEDC for buzzer control
  const int ledcChannel = 0;
  const int freq = 5000;
  const int resolution = 8;
  const int ledcPin = BUZZER_PIN;
  ledcSetup(ledcChannel, freq, resolution);
  ledcAttachPin(ledcPin, ledcChannel);
}

void loop() {
  if (rfid.PICC_IsNewCardPresent()) { // New tag is available
    if (rfid.PICC_ReadCardSerial()) { // Tag ID has been read
      String tagID = getTagID();
      sendTagID(tagID);
      
      // Produce buzzer sound
      buzzerSound();
    }
  }
}

String getTagID() {
  String tagID = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    tagID += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
    tagID += String(rfid.uid.uidByte[i], HEX);
  }
  return tagID;
}

void sendTagID(String tagID) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = String(HOST_NAME) + String(PATH_NAME) + "?uid=" + tagID; // Change "id" to "uid"
    Serial.print("Sending tag ID to server: ");
    Serial.println(url);
    http.begin(url);
    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Server response: ");
      Serial.println(response);
    } else {
      Serial.print("Error sending tag ID: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi not connected!");
  }
  delay(1000); // Adjust delay as needed to avoid sending tag ID multiple times
}

void buzzerSound() {
  const int ledcChannel = 0;
  const int dutyCycle = 128; // Adjust duty cycle as needed
  const int ledPin = 17; // Example LED pin, change to your setup
  pinMode(ledPin, OUTPUT);
  ledcSetup(ledcChannel, 5000, 8);
  ledcAttachPin(ledPin, ledcChannel);
  ledcWrite(ledcChannel, dutyCycle);
  delay(20); // Adjust delay as needed
  ledcWrite(ledcChannel, 0); // Turn off the LED
}

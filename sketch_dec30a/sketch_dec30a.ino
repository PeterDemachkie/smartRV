#include <HTTP_Method.h>
#include <Uri.h>
#include <WebServer.h>

#include <WiFi.h>

const char *ssid = "";
const char *password = "";

WebServer server(80);

const int greenButtonPin = 21;
const int redButtonPin = 5;
const int greenLedPin = 23;
const int redLedPin = 4;

bool greenButtonState = false;
bool redButtonState = false;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println("IP Address : ");
  IPAddress IP = WiFi.localIP();
  Serial.println(IP);
  // Start server
  server.on("/", HTTP_GET, handleRequest);
  server.begin();

  // Start server
  server.on("/", HTTP_GET, handleRequest);
  server.on("/heaterOn", HTTP_GET, heaterOn);
  server.on("/heaterOff", HTTP_GET, heaterOff);
  server.begin();

  // Set pins
  pinMode(greenButtonPin, INPUT_PULLUP);
  pinMode(redButtonPin, INPUT_PULLUP);
  pinMode(greenLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  
  // System starts with heater off
  digitalWrite(redLedPin, HIGH);
}

void loop() {
  // Read the state of the buttons
  server.handleClient();
  greenButtonState = digitalRead(greenButtonPin);
  redButtonState = digitalRead(redButtonPin);
  // Check the state of the green button
  if (greenButtonState == LOW) {
    digitalWrite(greenLedPin, HIGH);
    digitalWrite(redLedPin, LOW);
  }

  // Check the state of the red button
  if (redButtonState == LOW) {
    // Flash the red LED (adjust the delay for your desired flash rate)
    digitalWrite(redLedPin, HIGH);
    digitalWrite(greenLedPin, LOW);

  }
}

void handleRequest() {
  if (server.method() == HTTP_GET) {
    String response = "{ \"green\": " + String(digitalRead(greenLedPin)) +
                      ", \"red\": " + String(digitalRead(redLedPin)) + " }";
    server.send(200, "application/json", response);
  }
}

void heaterOn() {
  digitalWrite(greenLedPin, HIGH);
  digitalWrite(redLedPin, LOW);
  server.send(200, "text/plain", "heater turned on");
}

void heaterOff() {
  digitalWrite(greenLedPin, LOW);
  digitalWrite(redLedPin, HIGH);
  server.send(200, "text/plain", "heater turned off");
}


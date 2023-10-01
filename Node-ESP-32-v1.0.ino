#include <WiFi.h>
#include <ESPAsyncWebServer.h>

const char *ssid = "vks iPhone";
const char *password = "petronas";

AsyncWebServer server(80);

String receivedData = ""; // Store received data

void setup() {
  // Start Serial communication at 9600 baud
  Serial.begin(9600);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println("IP address: " + WiFi.localIP().toString());

  // Define the route for the web server
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    String html = "<html><body>";
    html += "<h1>ESP32 Serial Data</h1>";
    
    // JavaScript to auto-refresh the page every 5 seconds
    html += "<script>setTimeout(function(){ location.reload(); }, 5000);</script>";
    
    html += "<p>";
    
    // Read data from Serial and append it to the receivedData string
    while (Serial.available()) {
      char c = Serial.read();
      receivedData += c;
    }
    
    // Display the received data one below another
    html += receivedData;
    
    html += "</p></body></html>";
    request->send(200, "text/html", html);
  });

  // Start the web server
  server.begin();
}

void loop() {
  // You can add any other code you need here
}

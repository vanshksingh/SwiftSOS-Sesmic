#include <Wire.h>
#include <MPU6050.h>
#include <LiquidCrystal.h>

MPU6050 mpu;
float richter;

const int redLedPin = 8;    // Red LED Pin for high-intensity earthquakes (8-10)
const int yellowLedPin = 7; // Yellow LED Pin for medium-intensity earthquakes (4-7)
const int greenLedPin = 6;  // Green LED Pin for low-intensity earthquakes (1-3)
const int buzzerPin = 2;    // Buzzer Pin for high-intensity earthquakes (8-10)
const int soilMoisturePin = A15; // Soil Moisture Sensor Pin
int Contrast = 60;
const int rs = A3, en = A5, d4 = A9, d5 = A10, d6 = A11, d7 = A12;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Boot animation delay
const int animationDelay = 500; // Milliseconds per frame
const int numBootLoops = 2;

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud
  Wire.begin();
  mpu.initialize();
  analogWrite(9, Contrast);
  pinMode(A14, OUTPUT);
  pinMode(A13, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A0, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A1, OUTPUT);

  digitalWrite(A14, LOW);
  digitalWrite(A13, HIGH);
  digitalWrite(A4, LOW);
  digitalWrite(A0, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A1, HIGH);

  pinMode(redLedPin, OUTPUT);
  pinMode(yellowLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(soilMoisturePin, INPUT); // Set Soil Moisture Sensor Pin as an input
  Serial.println("Checking for earthquake and soil moisture...");
  lcd.begin(16, 2);
  
  // Display the "starting up" animation
  displayBootAnimation();
  
  // Display the welcome message
  displayWelcomeMessage();
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  int16_t totalAcceleration = abs(ax) + abs(ay);

  // Calculate Richter scale reading (adjust thresholds)
  float richter = map(totalAcceleration, 1500, 6800, 1, 10);

  // Ensure the Richter scale reading never goes above 10
  if (richter > 10.0) {
    richter = 10.0;
  }

  // Read Soil Moisture Sensor
  int soilMoistureValue = analogRead(soilMoisturePin);

  // Print Soil Moisture Reading
  Serial.print("Soil Moisture Reading: ");
  Serial.println(soilMoistureValue);

  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("SMR ");
  lcd.println(soilMoistureValue);

  // Print Richter scale reading
  Serial.print("Richter scale reading: ");
  Serial.println(richter);
  
  lcd.setCursor(0, 1);
  // Print a message to the LCD.
  lcd.print("RSR ");
  lcd.println(richter);

  // Determine the LED to light up based on earthquake intensity
  if (richter >= 5) { // High-intensity earthquake (8-10)
    digitalWrite(redLedPin, HIGH);
    digitalWrite(yellowLedPin, LOW);
    digitalWrite(greenLedPin, LOW);
    digitalWrite(buzzerPin, HIGH); // Activate the buzzer for high-intensity earthquakes
  } else if (richter >= 2 || 0) { // Medium-intensity earthquake (4-7)
    digitalWrite(redLedPin, LOW);
    digitalWrite(yellowLedPin, HIGH);
    digitalWrite(greenLedPin, LOW);
    digitalWrite(buzzerPin, LOW); // Deactivate the buzzer for medium-intensity earthquakes
  } else if (richter >= 1) { // Low-intensity earthquake (1-3)
    digitalWrite(redLedPin, LOW);
    digitalWrite(yellowLedPin, LOW);
    digitalWrite(greenLedPin, HIGH);
    digitalWrite(buzzerPin, LOW); // Deactivate the buzzer for low-intensity earthquakes
  } else { // No earthquake or very low-intensity
    digitalWrite(redLedPin, LOW);
    digitalWrite(yellowLedPin, LOW);
    digitalWrite(greenLedPin, LOW);
    digitalWrite(buzzerPin, LOW); // Deactivate the buzzer
  }

  // Control LED based on Soil Moisture
  if (soilMoistureValue < 500) {
    digitalWrite(redLedPin, HIGH);
    digitalWrite(yellowLedPin, LOW);
    digitalWrite(greenLedPin, LOW);
    digitalWrite(buzzerPin, HIGH); // Activate the buzzer for low soil moisture
  }

  // Delay before next reading
  delay(200); // Adjust as needed for desired update frequency
}

void displayBootAnimation() {
  for (int i = 0; i < numBootLoops; i++) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Starting up");
    delay(animationDelay);
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Starting up.");
    delay(animationDelay);
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Starting up..");
    delay(animationDelay);
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Starting up...");
    delay(animationDelay);
  }
}

void displayWelcomeMessage() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Welcome to NODE");
  delay(2000);
  lcd.setCursor(0, 1);
  lcd.print("by- SwiftSOS");
  delay(2000);
}

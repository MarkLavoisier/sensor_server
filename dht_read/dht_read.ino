#define DHTPIN A1     // what pin we're connected to
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"
// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x3F, 16, 2);//u need i2c scan
// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11
#define DHTTYPE DHT22   // DHT 22  (AM2302)
//Of all the sensors, this is the most precise and accurate. a dollar or two dollars.

//#define DHTTYPE DHT21   // DHT 21 (AM2301)
// Connect pin 1 (on the left) of the sensor to +5V
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor
int cpu_temp ;
float new_cpu_temp;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  // initialize the LCD
  lcd.begin();
  // Turn on the blacklight and print a message.
  lcd.backlight();
  lcd.print("Hello, sunghwan");
  lcd.setCursor(0, 1);
  lcd.print("roomSERVER v.2");
  delay(3000);
  lcd.clear();
}
void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  if (!(isnan(t) || isnan(h))) {
    //ex 56.85% 35.43 C => 56853543
    //Serial.print(h);Serial.print(t);
    float data_total = h * 1000000 + t * 100;
    Serial.println(data_total);
  }
  if (Serial.available()) {
    cpu_temp = Serial.parseInt();
  }
  if (cpu_temp > 99) {
    int one_h = cpu_temp / 100;
    int and_they = cpu_temp % 100;
    new_cpu_temp = and_they + (one_h * 0.1);
  }
  else {
    new_cpu_temp = cpu_temp;
  }
  lcd.print("temp "); lcd.print(t); lcd.print("/"); lcd.print(new_cpu_temp); lcd.print(" C");
  lcd.setCursor(0, 1);
  lcd.print("humd "); lcd.print(h); lcd.print(" %");
  lcd.setCursor(0, 0);
}

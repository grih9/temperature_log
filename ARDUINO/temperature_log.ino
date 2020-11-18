#include <Wire.h>
#include "Adafruit_MLX90614.h"

Adafruit_MLX90614 modIrTemp = Adafruit_MLX90614();

int red = 5;
int yellow = 6;
int green = 7;

void setup() {
  pinMode(red, OUTPUT); 
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  pinMode(8,OUTPUT);       
  digitalWrite(8,LOW);      
  modIrTemp.begin();  
  Serial.begin(9600);
}
bool flag = true;

void loop() {
  bool btnState = digitalRead(2);
  if (btnState && flag) {  
    Serial.println("start");
    flag = false;
    digitalWrite(yellow, HIGH);
    double sumreal = 0;
    double sum1 = 0;
    double sum2 = 0;
    double norm = 36.6;
  
    for (int i = 0; i < 10; i++) {
      double amb = modIrTemp.readAmbientTempC();
      double obj = modIrTemp.readObjectTempC();
      Serial.print("Ambient = "); Serial.print(amb); 
      Serial.print("*C\tObject = "); Serial.println(obj);
      double delta1 = obj - amb;
      double delta2 = norm - amb;
      double delta3 = norm - obj;
      sum1 += obj;
      sum2 += amb;
      sumreal += sqrt(amb * obj * 1.48);
      delay(100); // can adjust this for faster/slower updates
    }


    double temp1 = sumreal/10;
    double temp2 = sqrt((sum1 / 10) * (sum2 / 10) * 1.48);
    Serial.print("SumReal =");  Serial.print(temp1); Serial.print("\n");
    Serial.print("RealSum ="); Serial.print(temp2); Serial.print("\n");
    
    if ((temp1 < 35) || (temp1 > 45)) {
      for(int i = 0; i < 10; i++) {
        digitalWrite(yellow, HIGH);
        delay(50);
        digitalWrite(yellow, LOW);
        delay(50);
      }
    } else if (temp1 > 37.5) {
      for(int i = 0; i < 10; i++) {
        digitalWrite(red, HIGH);
        delay(50);
        digitalWrite(red, LOW);
        delay(50);
      }
    } else {
      for(int i = 0; i < 10; i++) {
        digitalWrite(green, HIGH);
        delay(50);
        digitalWrite(green, LOW);
        delay(50);
      }
    }
    digitalWrite(yellow, HIGH);
    delay(50);
    digitalWrite(yellow, LOW);
    delay(50);
    digitalWrite(yellow, HIGH);
  } else if (!btnState && !flag) {
    flag = true;
  }

  String read1;
  if (Serial.available() > 0) {
    read1 = Serial.readString();
    Serial.println(read1);
  }

  if (read1 == "not ok") {
    for(int i = 0; i < 10; i++) {
      digitalWrite(red, HIGH);
      delay(50);
      digitalWrite(red, LOW);
      delay(50);
    }
    digitalWrite(yellow, LOW);
  }
    if (read1 == "error") {
    for(int i = 0; i < 10; i++) {
      digitalWrite(yellow, HIGH);
      delay(50);
      digitalWrite(yellow, LOW);
      delay(50);
    }
  }
    if (read1 == "ok") {
    for(int i = 0; i < 10; i++) {
      digitalWrite(green, HIGH);
      delay(50);
      digitalWrite(green, LOW);
      delay(50);
    }
    digitalWrite(yellow, LOW);
  }
}

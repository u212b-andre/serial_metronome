#include "pitches.h"
#include <cmath>

int Numeratore = 0;
float msTempo = 0;
String fromPython_str = "";
char ch;
float fromPython = 0;

int suono[] = {
  NOTE_C4, NOTE_G3 // 262, 196
};

void setup() {
  Serial.begin(9600);
  
  float u1 = analogRead(A0) * (5.0 / 1024.0);
  float I = (5.0 - u1) / 1000;

  float u2 = analogRead(A2) * (5.0 / 1024.0);
  
  float numRes = ((u1 - u2) / I);
  float velRes = (u2 / I);
  
  Serial.print(numRes);
  Serial.print(",");
  Serial.println(velRes);
}

void loop() {

    while(Serial.available()){
      ch = Serial.read();
      fromPython_str += ch;
    }

    fromPython = fromPython_str.toFloat();
    msTempo = trunc(fromPython) / 100.0;
    Numeratore = round((fromPython / 100.0 - msTempo) * 10000);

    if (Numeratore != 0 && msTempo != 0){

      tone(8, suono[0], msTempo);
      delay(msTempo * 2.3);

      for (int j = 0; j != Numeratore - 1; j++){

        tone(8, suono[1], msTempo);
        delay(msTempo * 2.3);

      }     

      fromPython_str = "";
    
      float u1 = analogRead(A0) * (5.0 / 1024.0);
      float I = (5.0 - u1) / 1000;

      float u2 = analogRead(A2) * (5.0 / 1024.0);
  
      float numRes = ((u1 - u2) / I);
      float velRes = (u2 / I);
  
      Serial.print(numRes);
      Serial.print(",");
      Serial.println(velRes);
    
    }
  }
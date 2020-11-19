/* Encoder Library - Basic Example
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 *
 * This example code is in the public domain.
 */

#include <Encoder.h>

// Change these two numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder myEnc(5, 6);
//   avoid using pins with LEDs attached

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial1.write("Basic Encoder Test:");
  Serial.println("Basic Encoder Test:");
  
}
String msg = ""
long oldPosition  = -999;

void loop() {
  
  long newPosition = myEnc.read();
  if (newPosition != oldPosition) {
    oldPosition = newPosition;
    newPosition=newPosition/960;
    Serial.println(newPosition);
    Serial1.println(newPosition);
  }
}

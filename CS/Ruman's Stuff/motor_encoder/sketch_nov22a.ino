#include <i2c_t3.h>
#include <Encoder.h>

#define SLAVE_ADDRESS 0x29

// INIT PIXELS
void receiveEvent(size_t bytes);
void requestEvent(void);

// MEMORY
#define MEM_LEN 256
char databuf[MEM_LEN];
volatile uint8_t received;

Encoder myEnc(5, 6);
int led = 13;
// SETUP I2C AND PIXELS
void setup() 

{
  pinMode(led, OUTPUT);
  Wire1.begin(I2C_SLAVE, 0x29, I2C_PINS_22_23, I2C_PULLUP_EXT, 400000);
  received = 0;
  memset(databuf, 0, sizeof(databuf));
  Wire1.onReceive(receiveEvent);
  Wire1.onRequest(requestEvent);
  Serial.begin(9600);
  Serial.println("Basic Encoder Test:");
}
long oldPosition  = -999;


// LOOP
void loop() 
{
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
//  long newPosition = myEnc.read();
//  if (newPosition != oldPosition) {
//    oldPosition = newPosition;
//    newPosition=newPosition/960;
//    Serial.println(newPosition);
//    Wire1.write(newPosition);
//  }
}

// I2C DATA RECV CALLBACK
void receiveEvent(size_t bytes)
{
  Wire1.read(databuf, bytes);
  Serial.println(databuf[0]);
  received = bytes;
  //Serial.println("recv");
}

void requestEvent(void)
{
  long newPosition = myEnc.read();
  if (newPosition != oldPosition) {
//    oldPosition = newPosition;
//    newPosition=newPosition/960;
//    Serial.println(newPosition);
//    Wire1.write(newPosition);
  }
  oldPosition = newPosition;
  newPosition=newPosition/960;
  
  char *pos=convertToChararr(newPosition);
  Serial.println(pos);
  Wire1.write(pos,256);
  
  //Wire1.write(newPosition, MEM_LEN);
  //Serial.println("req..");
}
char* convertToChararr(long number)
{
  static char arr[32];
  for(int i=0;i<32;i++)
  {
    long mod=number % 255;
    number = floor(number/255);
    arr[i]= mod;
  }
  return arr;
}

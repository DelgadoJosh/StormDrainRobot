#include <i2c_t3.h>

#ifdef __AVR__
  #include <avr/power.h>
#endif

#define SLAVE_ADDRESS 0x29 

// Defining function names for callback
void receiveEvent(size_t bytes);
void requestEvent(void);

// MEMORY
#define MEM_LEN 256
char databuf[MEM_LEN];  // Databuffer
volatile uint8_t received;

// SETUP I2C
void setup() {
  Wire1.begin(I2C_SLAVE, SLAVE_ADDRESS, I2C_PINS_22_23, I2C_PULLUP_EXT, 400000);
  received = 0;
  memset(databuf, 0, sizeof(databuf));
  Wire1.onReceive(receiveEvent);
  Wire1.onRequest(requestEvent);
  Serial.begin(9600);
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1)
#endif 
}

// LOOP
void loop() {

}

void receiveEvent(size_t bytes) {
  Wire1.read(databuf, bytes);
  if (databuf[0] == 1) write = true;
  else write = false;
  Serial.println(databuf[0]);
  received = bytes; 
  Serial.println("recv");
}

void requestEvent(void) {
  Wire1.write(databuf, MEM_LEN);
  Serial.println("req..");
}

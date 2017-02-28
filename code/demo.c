/*
 * compile with :
 * gcc -Wall -lwiringPi -lwiringPiDev demo.c
 * 
 */

#include <wiringPi.h>
#include <piFace.h>

#define PIFACE 200
#define LED0 (PIFACE+0)
#define LED1 (PIFACE+1)
#define BUTTON0 (PIFACE+0)

int main(int argc, char* argv[]) {

  // Always initialise wiringPi. Use wiringPiSys() if you don't need
  // (or want) to run as root
  wiringPiSetupSys() ;

  // Setup the PiFace board
  piFaceSetup(PIFACE) ;
while (1) {
  if (digitalRead(BUTTON0) == LOW)
    digitalWrite(LED0, HIGH) ;
  else
    digitalWrite(LED0, LOW);
//  sleep(1);
}
  return 0;

}
